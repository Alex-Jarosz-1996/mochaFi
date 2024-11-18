import asyncio
import websockets
import json

class WebSocketTastyWorksClient:
    TIMEOUT = 5
    SETUP_CHANNEL = 0
    FEED_CHANNEL = 3
    
    def __init__(self, 
                 ws_url: str, 
                 session_token: str,
                 instrument_type: str,
                 instrument: str):
        
        self.ws_url = ws_url
        self.session_token = session_token
        self.instrument_type = instrument_type
        self.instrument = instrument

        if self.instrument_type not in ['stocks', 'options']:
            raise Exception("Improper instrument type choice. Choose either 'stocks' or 'options'.")

        self.setup_msg = {
            "type": "SETUP",
            "channel": self.SETUP_CHANNEL,
            "version": "0.1-DXF-JS/0.3.0",
            "keepaliveTimeout": self.TIMEOUT,
            "acceptKeepaliveTimeout": self.TIMEOUT
        }

        self.authorize_msg = {
            "type": "AUTH",
            "channel": self.SETUP_CHANNEL,
            "token": self.session_token
        }

        self.channel_request_msg = {
            "type": "CHANNEL_REQUEST",
            "channel": self.FEED_CHANNEL,
            "service": "FEED",
            "parameters": {
                "contract":"AUTO"
            }
        }

        self.feed_setup_msg = {
            "type": "FEED_SETUP",
            "channel": self.FEED_CHANNEL,
            "acceptAggregationPeriod": 0.1,
            "acceptDataFormat": "COMPACT",
            "acceptEventFields": {
                "Trade": ["eventSymbol", "price", "dayVolume", "size"],
                "Quote": ["eventSymbol", "bidPrice", "askPrice", "bidSize", "askSize"],
            }
        }

        if self.instrument_type == 'options':
            self.feed_setup_msg['acceptEventFields']['Greeks'] = ["eventSymbol", "volatility", "delta", "gamma", "theta", "rho", "vega"]   

        self.feed_subscription_msg = {
            "type": "FEED_SUBSCRIPTION",
            "channel": self.FEED_CHANNEL,
            "reset": True,
            "add": [
                {"type": "Trade", "symbol": instrument},
                {"type": "Quote", "symbol": instrument},
            ]
        }

        if self.instrument_type == 'options':
            self.feed_subscription_msg["add"].append({"type": "Greeks", "symbol": instrument})

        self.keep_alive_msg = {
            "type": "KEEPALIVE",
            "channel": self.FEED_CHANNEL
        }

    async def send_message(self, ws, message):
        """
        Sends a message to the WebSocket server.
        """
        await ws.send(json.dumps(message))
        print(f"Sent: {message}")

    async def receive_message(self, ws):
        """
        Continuously receives messages from the WebSocket server.
        """
        async for message in ws:
            print(f"Received: {message}")

    async def periodic_messages(self, ws, interval=1):
        """
        Periodically sends feed subscription and keep-alive messages every `interval` seconds.
        """
        while True:
            await asyncio.sleep(interval)
            await self.send_message(ws, self.feed_subscription_msg)
            await self.send_message(ws, self.keep_alive_msg)

    async def connect(self):
        """
        Connects to the websocket. 
        """
        async with websockets.connect(self.ws_url) as ws:
            # Step 1: Send the initial setup, authorization, channel request, and feed setup messages
            await self.send_message(ws, self.setup_msg)
            await self.send_message(ws, self.authorize_msg)
            await self.send_message(ws, self.channel_request_msg)
            await self.send_message(ws, self.feed_setup_msg)
            
            # Step 2: Start the periodic task for feed_subscription and keep_alive messages
            asyncio.create_task(self.periodic_messages(ws))

            # Continuously receive messages from the WebSocket server
            await self.receive_message(ws)

    def run_websocket_client(self):
        """
        Method responsible for receiving data stream.
        """
        asyncio.run(self.connect())
