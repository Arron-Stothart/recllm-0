import { useState } from 'react'
import { useRef } from 'react'
import { ChatInput } from './ChatInput'
import { Overview } from './Overview'
import { AnimatePresence } from 'framer-motion'
import { Message, ThinkingMessage } from './Message'
import { SearchInput } from './SearchInput'

interface Message {
  id: string
  content: string
  sender: 'user' | 'system'
}

export function Chat() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim()) return

    const userMessage: Message = {
      id: Date.now().toString(),
      content: input,
      sender: 'user'
    }

    setMessages(prev => [...prev, userMessage])
    setInput('')
    setIsLoading(true)

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: input })
      })

      const data = await response.json()
      
      const systemMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: data.response,
        sender: 'system'
      }

      setMessages(prev => [...prev, systemMessage])
    } catch (error) {
      console.error('Failed to send message:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleStop = () => {
    setIsLoading(false)
    // Add any additional stop logic here
  }

  return (
    <div className="py-4 h-full flex flex-col">
      <div className="mb-4 flex-1 flex flex-col">
        <AnimatePresence>
          {messages.length === 0 && (
            <div className="flex-1 flex items-center justify-center">
              <Overview />
            </div>
          )}
        </AnimatePresence>
        {messages.map((message) => (
          <Message
            key={message.id}
            id={message.id}
            content={message.content}
            sender={message.sender}
          />
        ))}
        {isLoading && <ThinkingMessage />}
      </div>

      <div className="flex-1 flex flex-row justify-center">
        <AnimatePresence mode="wait">
          {messages.length === 0 ? (
            <SearchInput key="search" query={input} setQuery={setInput} onSubmit={handleSubmit} />
          ) : (
            <ChatInput
              key="chat"
              input={input}
              setInput={setInput}
              isLoading={isLoading}
              onSubmit={handleSubmit}
              onStop={handleStop}
            />
          )}
        </AnimatePresence>
      </div>
    </div>
  )
} 