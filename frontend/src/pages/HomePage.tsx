import { useNavigate, useSearchParams } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import {
  Box,
  Button,
  Card,
  CircularProgress,
  Container,
  Divider,
  Pagination,
  Typography,
} from '@mui/material';
import { postService } from '@/services/postService';
import { PostRow } from '@/components/posts/PostRow';
import { useAuth } from '@/hooks/useAuth';
import { ROUTES } from '@/router/routes';

const HomePage = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [searchParams, setSearchParams] = useSearchParams();

  const search = searchParams.get('search') ?? undefined;
  const author = searchParams.get('author') ?? undefined;
  const dateFrom = searchParams.get('date_from') ?? undefined;
  const dateTo = searchParams.get('date_to') ?? undefined;
  const page = parseInt(searchParams.get('page') ?? '1', 10);

  const queryKey = { search, author, date_from: dateFrom, date_to: dateTo, page, page_size: 20 };

  const { data, isLoading } = useQuery({
    queryKey: ['posts', queryKey],
    queryFn: () => postService.listPosts(queryKey),
  });

  const posts = data?.data ?? [];
  const meta = data?.meta;
  const totalPages = meta?.total_pages ?? 1;

  const handlePageChange = (_: React.ChangeEvent<unknown>, newPage: number) => {
    const next = new URLSearchParams(searchParams);
    next.set('page', String(newPage));
    setSearchParams(next);
  };

  const hasFilters = search || author || dateFrom || dateTo;

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      {/* Page header */}
      <Box sx={{ mb: 3 }}>
        <Typography variant="h4" fontWeight={700}>
          Discussions
        </Typography>
        {hasFilters && (
          <Typography variant="body2" color="text.secondary" sx={{ mt: 0.5 }}>
            {meta?.total ?? 0} result{(meta?.total ?? 0) !== 1 ? 's' : ''} found
          </Typography>
        )}
      </Box>

      {/* Post list */}
      {isLoading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', mt: 8 }}>
          <CircularProgress />
        </Box>
      ) : posts.length === 0 ? (
        <Box sx={{ textAlign: 'center', mt: 10 }}>
          <Typography variant="h6" color="text.secondary" gutterBottom>
            {hasFilters ? 'No posts match your search.' : 'No discussions yet.'}
          </Typography>
          {user && !hasFilters && (
            <Button
              variant="contained"
              sx={{ mt: 2 }}
              onClick={() => navigate(ROUTES.CREATE_POST)}
            >
              Start the first discussion
            </Button>
          )}
        </Box>
      ) : (
        <>
          <Card elevation={0} sx={{ border: '1px solid', borderColor: 'divider', overflow: 'hidden' }}>
            {posts.map((post, index) => (
              <Box key={post.id}>
                {index > 0 && <Divider />}
                <PostRow post={post} queryKey={queryKey} />
              </Box>
            ))}
          </Card>

          {totalPages > 1 && (
            <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
              <Pagination
                count={totalPages}
                page={page}
                onChange={handlePageChange}
                color="primary"
                shape="rounded"
              />
            </Box>
          )}
        </>
      )}
    </Container>
  );
};

export default HomePage;
