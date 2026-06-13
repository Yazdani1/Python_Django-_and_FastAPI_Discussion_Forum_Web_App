import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { Box, Button, CircularProgress, Container, Pagination, Typography } from '@mui/material';
import { Add } from '@mui/icons-material';
import { postService } from '@/services/postService';
import { PostCard } from '@/components/posts/PostCard';
import { SearchBar } from '@/components/posts/SearchBar';
import { useAuth } from '@/hooks/useAuth';
import { ROUTES } from '@/router/routes';
import type { IPostSearchParams } from '@/types/post.types';

const HomePage = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [searchParams, setSearchParams] = useState<IPostSearchParams>({ page: 1, page_size: 20 });

  const { data, isLoading } = useQuery({
    queryKey: ['posts', searchParams],
    queryFn: () => postService.listPosts(searchParams),
  });

  const posts = data?.data ?? [];
  const meta = data?.meta;
  const totalPages = meta?.total_pages ?? 1;

  const handleSearch = (params: IPostSearchParams) => {
    setSearchParams((prev) => ({ ...prev, ...params }));
  };

  const handlePageChange = (_: React.ChangeEvent<unknown>, page: number) => {
    setSearchParams((prev) => ({ ...prev, page }));
  };

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" fontWeight={700}>
          Discussions
        </Typography>
        {user && (
          <Button variant="contained" startIcon={<Add />} onClick={() => navigate(ROUTES.CREATE_POST)}>
            New Post
          </Button>
        )}
      </Box>

      <SearchBar onSearch={handleSearch} initialParams={searchParams} />

      {isLoading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
          <CircularProgress />
        </Box>
      ) : posts.length === 0 ? (
        <Box sx={{ textAlign: 'center', mt: 8 }}>
          <Typography variant="h6" color="text.secondary">
            No posts found.
          </Typography>
          {user && (
            <Button variant="contained" sx={{ mt: 2 }} onClick={() => navigate(ROUTES.CREATE_POST)}>
              Be the first to post!
            </Button>
          )}
        </Box>
      ) : (
        <>
          {posts.map((post) => (
            <PostCard key={post.id} post={post} />
          ))}

          {totalPages > 1 && (
            <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
              <Pagination
                count={totalPages}
                page={searchParams.page ?? 1}
                onChange={handlePageChange}
                color="primary"
              />
            </Box>
          )}
        </>
      )}
    </Container>
  );
};

export default HomePage;
