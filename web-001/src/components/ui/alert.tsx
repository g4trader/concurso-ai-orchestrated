import { HTMLAttributes, forwardRef } from 'react'
import { clsx } from 'clsx'

interface AlertProps extends HTMLAttributes<HTMLDivElement> {
  variant?: 'default' | 'destructive'
}

export const Alert = forwardRef<HTMLDivElement, AlertProps>(
  ({ className, variant = 'default', ...props }, ref) => {
    return (
      <div
        ref={ref}
        className={clsx(
          'rounded-lg border p-4',
          {
            'border-gray-200 bg-white text-gray-900': variant === 'default',
            'border-red-200 bg-red-50 text-red-900': variant === 'destructive',
          },
          className
        )}
        {...props}
      />
    )
  }
)

Alert.displayName = 'Alert'
