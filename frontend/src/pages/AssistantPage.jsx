import React, { useState, useRef, useEffect } from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import DashboardLayout from '../components/DashboardLayout';
import { useAssistant } from '../context/AssistantContext';
import { assistantService } from '../services/api';

const ChatContainer = styled.div`
  display: flex;
  flex-direction: column;
  height: calc(100vh - 220px);
  min-height: 400px;
  background: ${({ theme }) => theme.colors.bg.surface};
  border-radius: 16px;
  border: 1px solid ${({ theme }) => theme.colors.border};
  box-shadow: ${({ theme }) => theme.shadows.soft};
  overflow: hidden;
`;

const MessagesArea = styled.div`
  flex: 1;
  overflow-y: auto;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
`;

const Bubble = styled.div`
  max-width: 70%;
  padding: 1rem 1.25rem;
  border-radius: 14px;
  font-size: 0.95rem;
  line-height: 1.6;
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
  padding: 1rem 1.25rem;
  background: ${({ theme }) => theme.colors.bg.secondary};
  border-radius: 14px;
  font-size: 0.9rem;
  color: ${({ theme }) => theme.colors.text.secondary};
  font-style: italic;
`;

const ChipsRow = styled.div`
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid ${({ theme }) => theme.colors.border};
`;

const Chip = styled(motion.button)`
  padding: 0.5rem 1rem;
  border-radius: 20px;
  border: 1px solid ${({ theme }) => theme.colors.brand.primary};
  background: ${({ theme }) => theme.colors.brand.washed};
  color: ${({ theme }) => theme.colors.brand.dark};
  font-size: 0.85rem;
  font-weight: 500;
  cursor: pointer;
  white-space: nowrap;

  &:hover {
    background: ${({ theme }) => theme.colors.brand.primary};
    color: white;
  }
`;

const InputBar = styled.form`
  display: flex;
  padding: 1rem 1.5rem;
  border-top: 1px solid ${({ theme }) => theme.colors.border};
  gap: 0.75rem;
`;

const ChatInput = styled.input`
  flex: 1;
  padding: 0.75rem 1rem;
  border: 1px solid ${({ theme }) => theme.colors.border};
  border-radius: 10px;
  font-size: 1rem;
  background: ${({ theme }) => theme.colors.bg.primary};
  color: ${({ theme }) => theme.colors.text.primary};

  &:focus {
    outline: none;
    border-color: ${({ theme }) => theme.colors.brand.primary};
    box-shadow: 0 0 0 3px ${({ theme }) => theme.colors.brand.washed};
  }
`;

const SendBtn = styled.button`
  padding: 0.75rem 1.5rem;
  background: ${({ theme }) => theme.colors.brand.primary};
  color: white;
  border: none;
  border-radius: 10px;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  &:hover:not(:disabled) {
    background: ${({ theme }) => theme.colors.brand.dark};
  }
`;

const SUGGESTION_CHIPS = [
  'What bills are currently open?',
  'How do I submit feedback?',
  'Explain the Finance Bill',
  'What are my rights as a citizen?',
  'Summarise public sentiment',
];

function AssistantPage() {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      text: 'Jambo! I\'m Jamii Assistant, your civic engagement guide. Ask me about active legislation, how to participate in public feedback, your rights under the Constitution, or anything about governance in Kenya.\n\nTry one of the suggestions above or type your own question.',
    },
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const { activeInstrumentId } = useAssistant();

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const sendMessage = async (text) => {
    if (!text.trim() || loading) return;

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

  const handleSubmit = (e) => {
    e.preventDefault();
    sendMessage(input);
  };

  return (
    <DashboardLayout title="Jamii Assistant" subtitle="Your AI-powered civic engagement guide.">
      <ChatContainer>
        <ChipsRow>
          {SUGGESTION_CHIPS.map((chip) => (
            <Chip
              key={chip}
              onClick={() => sendMessage(chip)}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              disabled={loading}
            >
              {chip}
            </Chip>
          ))}
        </ChipsRow>

        <MessagesArea>
          {messages.map((msg, i) => (
            <Bubble key={i} role={msg.role}>
              {msg.text}
            </Bubble>
          ))}
          {loading && <TypingIndicator>Jamii Assistant is thinking...</TypingIndicator>}
          <div ref={messagesEndRef} />
        </MessagesArea>

        <InputBar onSubmit={handleSubmit}>
          <ChatInput
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask about legislation, civic rights, feedback..."
            disabled={loading}
          />
          <SendBtn type="submit" disabled={loading || !input.trim()}>
            Send
          </SendBtn>
        </InputBar>
      </ChatContainer>
    </DashboardLayout>
  );
}

export default AssistantPage;
