import { HTMLAttributes } from 'react'
import { clsx } from 'clsx'

interface SpinnerProps extends HTMLAttributes<HTMLDivElement> {
  size?: 'sm' | 'md' | 'lg'
}

export function Spinner({ className, size = 'md', ...props }: SpinnerProps) {
  return (
    <div
      className={clsx(
        'animate-spin rounded-full border-2 border-gray-300 border-t-primary-600',
        {
          'h-4 w-4': size === 'sm',
          'h-6 w-6': size === 'md',
          'h-8 w-8': size === 'lg',
        },
        className
      )}
      {...props}
    />
  )
}
