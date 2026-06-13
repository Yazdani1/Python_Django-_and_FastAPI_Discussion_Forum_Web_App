import { useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import { Box, Button, CircularProgress, Container, Typography } from '@mui/material';
import { ArrowBack } from '@mui/icons-material';
import { postService } from '@/services/postService';
import { PostForm } from '@/components/posts/PostForm';
import { ROUTES } from '@/router/routes';
import type { TPostFormValues } from '@/components/posts/PostForm';

const EditPostPage = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const [isSubmitting, setIsSubmitting] = useState(false);

  const { data: res, isLoading } = useQuery({
    queryKey: ['post', id],
    queryFn: () => postService.getPost(id!),
    enabled: !!id,
  });

  const post = res?.data;

  const handleSubmit = async (data: TPostFormValues) => {
    if (!id) return;
    setIsSubmitting(true);
    try {
      await postService.updatePost(id, data);
      queryClient.invalidateQueries({ queryKey: ['post', id] });
      queryClient.invalidateQueries({ queryKey: ['posts'] });
      navigate(ROUTES.POST_DETAIL(id));
    } finally {
      setIsSubmitting(false);
    }
  };

  if (isLoading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', mt: 8 }}>
        <CircularProgress />
      </Box>
    );
  }

  if (!post) {
    return (
      <Container maxWidth="md" sx={{ py: 4 }}>
        <Typography color="error">Post not found.</Typography>
      </Container>
    );
  }

  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <Button
        startIcon={<ArrowBack />}
        onClick={() => navigate(ROUTES.POST_DETAIL(id!))}
        sx={{ mb: 3 }}
      >
        Back to Post
      </Button>

      <Typography variant="h4" fontWeight={700} gutterBottom>
        Edit Post
      </Typography>

      <PostForm
        defaultValues={{ title: post.title, content: post.content }}
        onSubmit={handleSubmit}
        submitLabel="Save Changes"
        isSubmitting={isSubmitting}
      />
    </Container>
  );
};

export default EditPostPage;
