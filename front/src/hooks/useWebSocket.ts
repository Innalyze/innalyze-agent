import { useEffect, useRef, useCallback } from "react";

interface WebSocketHookOptions {
  onMessage: (data: string) => void;
  onError?: (error: Event) => void;
  onClose?: () => void;
}

export const useWebSocket = (url: string, options: WebSocketHookOptions) => {
  const ws = useRef<WebSocket | null>(null);

  // Function to initialize a new WebSocket connection
  const initializeWebSocket = useCallback(() => {
    const socket = new WebSocket(url);
    ws.current = socket;

    socket.onmessage = (event) => {
      options.onMessage(event.data);
    };

    socket.onerror = (error) => {
      if (options.onError) {
        options.onError(error);
      }
    };

    socket.onclose = () => {
      if (options.onClose) {
        options.onClose();
      }
    };

    return socket;
  }, [url, options]);

  // Send a message and handle reconnection
  const sendMessage = useCallback(
    (message: string) => {
      // Close the existing connection if it exists
      if (ws.current) {
        ws.current.close();
      }

      // Initialize a new WebSocket connection
      const socket = initializeWebSocket();

      // Send the message once the connection is open
      socket.onopen = () => {
        socket.send(message);
      };
    },
    [initializeWebSocket]
  );

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (ws.current) {
        ws.current.close();
      }
    };
  }, []);

  return { sendMessage };
};
