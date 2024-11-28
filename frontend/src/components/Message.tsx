'use client';

import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';
import { Sparkles, ThumbsUp, ThumbsDown } from 'lucide-react';

interface MessageProps {
  id: string;
  content: string;
  sender: 'user' | 'system';
}

export function Message({ id, content, sender }: MessageProps) {
  const handleLike = () => {
    // TODO: Implement like functionality
    console.log('Liked message:', id);
  };

  const handleDislike = () => {
    // TODO: Implement dislike functionality
    console.log('Disliked message:', id);
  };

  return (
    <motion.div
      className="w-full mx-auto max-w-3xl px-4 group/message"
      initial={{ y: 5, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      data-role={sender === 'user' ? 'user' : 'assistant'}
    >
      <div
        className={cn(
          'flex gap-4 w-full',
          sender === 'user' 
            ? 'bg-primary text-primary-foreground px-3 w-fit ml-auto max-w-2xl py-2 rounded-lg' 
            : ''
        )}
      >
        {sender === 'system' && (
          <div className="size-8 flex items-center rounded-full justify-center ring-1 shrink-0 ring-border bg-primary/5">
            <Sparkles className="size-4 text-primary" />
          </div>
        )}

        <div className="flex flex-col gap-2 w-full">
          <div className="flex flex-col gap-4">
            {content}
          </div>
          {sender === 'system' && (
            <div className="flex gap-2 items-center mt-2">
              <button
                onClick={handleLike}
                className="p-1 hover:bg-primary/10 rounded-md transition-colors"
                aria-label="Like message"
              >
                <ThumbsUp className="size-4" />
              </button>
              <button
                onClick={handleDislike}
                className="p-1 hover:bg-primary/10 rounded-md transition-colors"
                aria-label="Dislike message"
              >
                <ThumbsDown className="size-4" />
              </button>
            </div>
          )}
        </div>
      </div>
    </motion.div>
  );
}

export function ThinkingMessage() {
  return (
    <motion.div
      className="w-full mx-auto max-w-3xl px-4 group/message"
      initial={{ y: 5, opacity: 0 }}
      animate={{ y: 0, opacity: 1, transition: { delay: 1 } }}
      data-role="assistant"
    >
      <div className="flex gap-4 w-full">
        <div className="size-8 flex items-center rounded-full justify-center ring-1 shrink-0 ring-border bg-primary/5">
          <Sparkles className="size-4 text-primary" />
        </div>

        <div className="flex flex-col gap-2 w-full">
          <div className="flex flex-col gap-4 text-muted-foreground">
            Thinking...
          </div>
        </div>
      </div>
    </motion.div>
  );
}