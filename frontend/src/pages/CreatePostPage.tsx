import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useQueryClient } from '@tanstack/react-query';
import { Box, Button, Container, Typography } from '@mui/material';
import { ArrowBack } from '@mui/icons-material';
import { postService } from '@/services/postService';
import { PostForm } from '@/components/posts/PostForm';
import { ROUTES } from '@/router/routes';
import type { TPostFormValues } from '@/components/posts/PostForm';

const CreatePostPage = () => {
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (data: TPostFormValues) => {
    setIsSubmitting(true);
    try {
      const res = await postService.createPost(data);
      queryClient.invalidateQueries({ queryKey: ['posts'] });
      if (res.data) navigate(ROUTES.POST_DETAIL(res.data.id));
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <Button startIcon={<ArrowBack />} onClick={() => navigate(ROUTES.HOME)} sx={{ mb: 3 }}>
        Back
      </Button>

      <Typography variant="h4" fontWeight={700} gutterBottom>
        Create New Post
      </Typography>

      <PostForm onSubmit={handleSubmit} submitLabel="Publish Post" isSubmitting={isSubmitting} />
    </Container>
  );
};

export default CreatePostPage;
