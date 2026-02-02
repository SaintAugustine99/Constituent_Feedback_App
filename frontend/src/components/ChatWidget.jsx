import React, { useState, useRef, useEffect } from 'react';
import styled from 'styled-components';
import { motion, AnimatePresence } from 'framer-motion';
import { useLocation } from 'react-router-dom';
import { useAssistant } from '../context/AssistantContext';
import { assistantService } from '../services/api';

const Fab = styled(motion.button)`
  position: fixed;
  bottom: 24px;
  right: 24px;
  width: 56px;
  height: 56px;
  border-radius: 50%;
  border: none;
  background: ${({ theme }) => theme.colors.brand.primary};
  color: white;
  font-size: 1.5rem;
  cursor: pointer;
  box-shadow: 0 4px 20px rgba(85, 107, 47, 0.4);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;

  &:hover {
    background: ${({ theme }) => theme.colors.brand.dark};
  }
`;

const Panel = styled(motion.div)`
  position: fixed;
  bottom: 90px;
  right: 24px;
  width: 380px;
  height: 500px;
  background: ${({ theme }) => theme.colors.bg.surface};
  border-radius: 16px;
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
  border: 1px solid ${({ theme }) => theme.colors.border};
  z-index: 1000;
  display: flex;
  flex-direction: column;
  overflow: hidden;

  @media (max-width: 480px) {
    width: calc(100vw - 32px);
    right: 16px;
    bottom: 84px;
    height: 60vh;
  }
`;

const PanelHeader = styled.div`
  padding: 1rem 1.25rem;
  background: ${({ theme }) => theme.colors.brand.primary};
  color: white;
  font-family: ${({ theme }) => theme.fonts.heading};
  font-weight: 700;
  font-size: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
`;

const CloseBtn = styled.button`
  background: none;
  border: none;
  color: white;
  font-size: 1.2rem;
  cursor: pointer;
  padding: 0;
  line-height: 1;
`;

const MessagesArea = styled.div`
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
`;

const Bubble = styled.div`
  max-width: 85%;
  padding: 0.75rem 1rem;
  border-radius: 12px;
  font-size: 0.9rem;
  line-height: 1.5;
  white-space: pre-wrap;
  word-wrap: break-word;

  ${({ role, theme }) =>
    role === 'user'
      ? `
    align-self: flex-end;
    background: ${theme.colors.brand.primary};
    color: white;
    border-bottom-right-radius: 4px;
  `
      : `
    align-self: flex-start;
    background: ${theme.colors.bg.secondary};
    color: ${theme.colors.text.primary};
    border-bottom-left-radius: 4px;
  `}
`;

const TypingIndicator = styled.div`
  align-self: flex-start;
  padding: 0.75rem 1rem;
  background: ${({ theme }) => theme.colors.bg.secondary};
  border-radius: 12px;
  font-size: 0.85rem;
  color: ${({ theme }) => theme.colors.text.secondary};
  font-style: italic;
`;

const InputBar = styled.form`
  display: flex;
  padding: 0.75rem;
  border-top: 1px solid ${({ theme }) => theme.colors.border};
  gap: 0.5rem;
`;

const ChatInput = styled.input`
  flex: 1;
  padding: 0.6rem 0.8rem;
  border: 1px solid ${({ theme }) => theme.colors.border};
  border-radius: 8px;
  font-size: 0.9rem;
  background: ${({ theme }) => theme.colors.bg.primary};
  color: ${({ theme }) => theme.colors.text.primary};

  &:focus {
    outline: none;
    border-color: ${({ theme }) => theme.colors.brand.primary};
  }
`;

const SendBtn = styled.button`
  padding: 0.6rem 1rem;
  background: ${({ theme }) => theme.colors.brand.primary};
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  &:hover:not(:disabled) {
    background: ${({ theme }) => theme.colors.brand.dark};
  }
`;

function ChatWidget() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    { role: 'assistant', text: 'Jambo! I\'m Jamii Assistant. Ask me about any active bills, how to submit feedback, or anything about civic participation in Kenya.' },
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const location = useLocation();
  const { activeInstrumentId } = useAssistant();

  // Hide on /assistant page (full page has its own chat)
  if (location.pathname === '/assistant') return null;

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const handleSend = async (e) => {
    e.preventDefault();
    const text = input.trim();
    if (!text || loading) return;

    setMessages((prev) => [...prev, { role: 'user', text }]);
    setInput('');
    setLoading(true);

    try {
      const data = await assistantService.chat(text, activeInstrumentId);
      setMessages((prev) => [...prev, { role: 'assistant', text: data.reply }]);
    } catch {
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', text: 'Sorry, I encountered an error. Please try again.' },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <AnimatePresence>
        {isOpen && (
          <Panel
            initial={{ opacity: 0, y: 20, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 20, scale: 0.95 }}
            transition={{ duration: 0.2 }}
          >
            <PanelHeader>
              Jamii Assistant
              <CloseBtn onClick={() => setIsOpen(false)}>&times;</CloseBtn>
            </PanelHeader>

            <MessagesArea>
              {messages.map((msg, i) => (
                <Bubble key={i} role={msg.role}>
                  {msg.text}
                </Bubble>
              ))}
              {loading && <TypingIndicator>Jamii Assistant is thinking...</TypingIndicator>}
              <div ref={messagesEndRef} />
            </MessagesArea>

            <InputBar onSubmit={handleSend}>
              <ChatInput
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Ask about bills, feedback..."
                disabled={loading}
              />
              <SendBtn type="submit" disabled={loading || !input.trim()}>
                Send
              </SendBtn>
            </InputBar>
          </Panel>
        )}
      </AnimatePresence>

      <Fab
        onClick={() => setIsOpen(!isOpen)}
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.9 }}
        title="Chat with Jamii Assistant"
      >
        {isOpen ? '\u2715' : '\u{1F4AC}'}
      </Fab>
    </>
  );
}

export default ChatWidget;
