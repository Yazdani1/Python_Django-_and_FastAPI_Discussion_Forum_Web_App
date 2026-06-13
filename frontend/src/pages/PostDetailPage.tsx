import { useNavigate, useParams } from 'react-router-dom';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import {
  Avatar,
  Box,
  Button,
  CircularProgress,
  Container,
  Divider,
  Paper,
  Typography,
} from '@mui/material';
import { ArrowBack, Delete, Edit } from '@mui/icons-material';
import { postService } from '@/services/postService';
import { useAuth } from '@/hooks/useAuth';
import { ROUTES } from '@/router/routes';

const PostDetailPage = () => {
  const { id } = useParams<{ id: string }>();
  const { user } = useAuth();
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const { data: res, isLoading } = useQuery({
    queryKey: ['post', id],
    queryFn: () => postService.getPost(id!),
    enabled: !!id,
  });

  const deleteMutation = useMutation({
    mutationFn: () => postService.deletePost(id!),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['posts'] });
      navigate(ROUTES.HOME);
    },
  });

  const post = res?.data;

  if (isLoading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', mt: 8 }}>
        <CircularProgress />
      </Box>
    );
  }

  if (!post) {
    return (
      <Container maxWidth="lg" sx={{ py: 4 }}>
        <Typography color="error">Post not found.</Typography>
      </Container>
    );
  }

  const isOwner = user?.id === post.author.id;
  const isPrivileged = user?.role === 'moderator' || user?.role === 'admin';
  const canEdit = isOwner || isPrivileged;

  const formattedDate = new Date(post.created_at).toLocaleDateString('en-US', {
    year: 'numeric', month: 'long', day: 'numeric',
  });

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Button startIcon={<ArrowBack />} onClick={() => navigate(ROUTES.HOME)} sx={{ mb: 3 }}>
        Back to Discussions
      </Button>

      <Paper elevation={2} sx={{ p: 4 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
          <Typography variant="h4" fontWeight={700} sx={{ flexGrow: 1, pr: 2 }}>
            {post.title}
          </Typography>

          {canEdit && (
            <Box sx={{ display: 'flex', gap: 1 }}>
              <Button
                startIcon={<Edit />}
                variant="outlined"
                size="small"
                onClick={() => navigate(ROUTES.EDIT_POST(post.id))}
              >
                Edit
              </Button>
              <Button
                startIcon={<Delete />}
                variant="outlined"
                color="error"
                size="small"
                onClick={() => deleteMutation.mutate()}
                disabled={deleteMutation.isPending}
              >
                Delete
              </Button>
            </Box>
          )}
        </Box>

        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 3 }}>
          <Avatar
            src={post.author.avatar_url ?? undefined}
            sx={{ width: 28, height: 28, bgcolor: 'secondary.main', fontSize: 13 }}
          >
            {post.author.username[0].toUpperCase()}
          </Avatar>
          <Typography variant="body2" color="text.secondary">
            {post.author.username} · {formattedDate}
          </Typography>
        </Box>

        <Divider sx={{ mb: 3 }} />

        <Typography variant="body1" sx={{ whiteSpace: 'pre-wrap', lineHeight: 1.8 }}>
          {post.content}
        </Typography>
      </Paper>
    </Container>
  );
};

export default PostDetailPage;
