import { useRef } from 'react'
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Search } from "lucide-react"
import { motion } from 'framer-motion'

interface SearchInputProps {
  query: string
  setQuery: (value: string) => void
  isLoading?: boolean
  onSubmit: (e: React.FormEvent) => Promise<void>
}

export function SearchInput({ query, setQuery, isLoading, onSubmit }: SearchInputProps) {
  const inputRef = useRef<HTMLInputElement>(null)

  const handleKeyDown = (event: React.KeyboardEvent) => {
    if (event.key === 'Enter') {
      event.preventDefault()
      if (!isLoading) {
        onSubmit(event)
      }
    }
  }

  return (
    <motion.form 
      onSubmit={onSubmit} 
      className="flex w-full max-w-[640px] relative"
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: 10 }}
      transition={{ delay: 0.5 }}
    >
      <Input
        ref={inputRef}
        placeholder="Search"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        className="w-full h-10 pl-4 pr-14 rounded-full dark:bg-zinc-900 dark:border-zinc-700"
        autoFocus
        onKeyDown={handleKeyDown}
        disabled={isLoading}
      />
      <Button
        type="submit"
        variant="ghost"
        className="absolute right-0 h-10 pr-8 pl-6 rounded-r-full bg-gray-100 dark:bg-zinc-800 hover:bg-gray-200 dark:hover:bg-zinc-700 border-l border-gray-200 dark:border-zinc-700"
        disabled={query.length === 0 || isLoading}
      >
        <Search className="h-4 w-4" />
      </Button>
    </motion.form>
  )
}
