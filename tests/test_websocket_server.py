import pytest
from fastapi.testclient import TestClient
from src.communication.websocket_server import app, ConnectionManager

@pytest.fixture
def client():
    return TestClient(app)

def test_websocket_connection():
    client = TestClient(app)
    with client.websocket_connect("/ws/1") as websocket:
        data = websocket.receive_text()
        assert data == "Client #1 joined the chat"

def test_websocket_send_and_receive():
    client = TestClient(app)
    with client.websocket_connect("/ws/1") as websocket:
        websocket.send_text("Hello")
        data = websocket.receive_text()
        assert data == "You wrote: Hello"
        data = websocket.receive_text()
        assert data == "Client #1 says: Hello"

def test_websocket_broadcast():
    manager = ConnectionManager()
    client1 = TestClient(app)
    client2 = TestClient(app)
    
    with client1.websocket_connect("/ws/1") as websocket1, \
         client2.websocket_connect("/ws/2") as websocket2:
        
        websocket1.send_text("Hello from client 1")
        
        assert websocket1.receive_text() == "You wrote: Hello from client 1"
        assert websocket1.receive_text() == "Client #1 says: Hello from client 1"
        assert websocket2.receive_text() == "Client #1 says: Hello from client 1"

def test_websocket_disconnect():
    client = TestClient(app)
    with client.websocket_connect("/ws/1") as websocket:
        pass  # WebSocket will be closed when exiting the context
    
    # Try to send a message after disconnection
    with pytest.raises(Exception):
        websocket.send_text("This should fail")

if __name__ == "__main__":
    pytest.main([__file__])
