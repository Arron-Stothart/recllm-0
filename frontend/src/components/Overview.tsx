import { motion } from 'framer-motion';
import Link from 'next/link';

export const Overview = () => {
  return (
    <motion.div
      key="overview"
      className="max-w-3xl mx-auto md:mt-20"
      initial={{ opacity: 0, scale: 0.98 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.98 }}
      transition={{ delay: 0.5 }}
    >
      <div className="rounded-xl p-6 flex flex-col gap-8 leading-relaxed text-center max-w-xl">
        <p className="flex flex-row justify-center gap-2 items-center">
          <svg 
            xmlns="http://www.w3.org/2000/svg" 
            viewBox="0 0 24 24" 
            className="w-6 h-6 fill-current"
          >
            <path d="M19.615 3.184c-3.604-.246-11.631-.245-15.23 0-3.897.266-4.356 2.62-4.385 8.816.029 6.185.484 8.549 4.385 8.816 3.6.245 11.626.246 15.23 0 3.897-.266 4.356-2.62 4.385-8.816-.029-6.185-.484-8.549-4.385-8.816zm-10.615 12.816v-8l8 3.993-8 4.007z"/>
          </svg>
          RecLLM
        </p>
        {/* <p>
          This is an implementation of{' '}
          <Link
            className="font-medium underline underline-offset-4"
            href="https://arxiv.org/abs/2305.07961"
            target="_blank"
          >
            RecLLM
          </Link>{', '}
          a conversation layer for refining youtube recommendations through multi turn dialogues.
          the{' '}
          <code className="rounded-md bg-muted px-1 py-0.5">streamText</code>{' '}
          function in the server and the{' '}
          <code className="rounded-md bg-muted px-1 py-0.5">useChat</code> hook
          on the client to create a seamless chat experience.
        </p>
        <p>
          Start a conversation to get video recommendations.
        </p> */}
      </div>
    </motion.div>
  );
};