import { useRef } from 'react'
import { Textarea } from "@/components/ui/textarea"
import { Button } from "@/components/ui/button"
import { PauseIcon, ArrowUpIcon } from "lucide-react"

interface ChatInputProps {
  input: string
  setInput: (value: string) => void
  isLoading: boolean
  onSubmit: (e: React.FormEvent) => Promise<void>
  onStop?: () => void
}

export function ChatInput({ input, setInput, isLoading, onSubmit, onStop }: ChatInputProps) {
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  const handleKeyDown = (event: React.KeyboardEvent) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault()
      if (!isLoading) {
        onSubmit(event)
      }
    }
  }

  return (
    <form onSubmit={onSubmit} className="relative">
      <Textarea
        ref={textareaRef}
        placeholder="Send a message..."
        value={input}
        onChange={(e) => setInput(e.target.value)}
        className="min-h-[24px] max-h-[calc(75dvh)] pr-12 overflow-hidden resize-none rounded-xl text-base bg-muted"
        rows={3}
        autoFocus
        onKeyDown={handleKeyDown}
        disabled={isLoading}
      />
      {isLoading ? (
        <Button
          className="rounded-full p-1.5 h-fit absolute bottom-2 right-2 m-0.5 border dark:border-zinc-600"
          onClick={(event) => {
            event.preventDefault()
            onStop?.()
          }}
        >
          <PauseIcon size={14} />
        </Button>
      ) : (
        <Button
          className="rounded-full p-1.5 h-fit absolute bottom-2 right-2 m-0.5 border dark:border-zinc-600"
          onClick={(event) => {
            event.preventDefault()
            onSubmit(event)
          }}
          disabled={input.length === 0}
        >
          <ArrowUpIcon size={14} />
        </Button>
      )}
    </form>
  )
} 