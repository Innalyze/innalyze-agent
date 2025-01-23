let messageCounter = 0;

export const generateMessageId = (prefix: string = 'msg'): string => {
  messageCounter += 1;
  return `${prefix}_${Date.now()}_${messageCounter}`;
};