import { type FC, type ReactNode } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5,
      retry: (failureCount, error) => {
        if ((error as { statusCode?: number })?.statusCode === 401) return false;
        if ((error as { statusCode?: number })?.statusCode === 403) return false;
        return failureCount < 2;
      },
    },
  },
});

interface IQueryProviderProps {
  children: ReactNode;
}

export const QueryProvider: FC<IQueryProviderProps> = ({ children }) => {
  return (
    <QueryClientProvider client={queryClient}>
      {children}
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  );
};
