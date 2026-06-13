import { useRef, useState } from 'react';
import { zodResolver } from '@hookform/resolvers/zod';
import { useForm } from 'react-hook-form';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { z } from 'zod';
import {
  Avatar,
  Box,
  Button,
  Chip,
  CircularProgress,
  Container,
  Divider,
  Grid,
  IconButton,
  Paper,
  TextField,
  Typography,
} from '@mui/material';
import { CameraAlt, Edit } from '@mui/icons-material';
import { userService } from '@/services/userService';
import { useAuth } from '@/hooks/useAuth';
import type { IUserUpdateRequest } from '@/types/user.types';

const profileSchema = z.object({
  username: z
    .string()
    .min(3, 'At least 3 characters')
    .max(50, 'At most 50 characters')
    .regex(/^[a-zA-Z0-9_]+$/, 'Only letters, numbers, underscores')
    .optional()
    .or(z.literal('')),
  bio: z.string().max(500, 'Bio too long').optional(),
});

type TProfileForm = z.infer<typeof profileSchema>;

const ProfilePage = () => {
  const { setUser } = useAuth();
  const queryClient = useQueryClient();
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [isEditing, setIsEditing] = useState(false);

  const { data: profileRes, isLoading } = useQuery({
    queryKey: ['profile'],
    queryFn: () => userService.getProfile(),
  });

  const profile = profileRes?.data;

  const { register, handleSubmit, formState: { errors } } = useForm<TProfileForm>({
    resolver: zodResolver(profileSchema),
    values: { username: profile?.username ?? '', bio: profile?.bio ?? '' },
  });

  const updateMutation = useMutation({
    mutationFn: (data: IUserUpdateRequest) => userService.updateProfile(data),
    onSuccess: (res) => {
      if (res.data) {
        setUser({ id: res.data.id, email: res.data.email, username: res.data.username, role: res.data.role, avatar_url: res.data.avatar_url });
        queryClient.invalidateQueries({ queryKey: ['profile'] });
      }
      setIsEditing(false);
    },
  });

  const avatarMutation = useMutation({
    mutationFn: (file: File) => userService.uploadAvatar(file),
    onSuccess: (res) => {
      if (res.data) {
        setUser({ id: res.data.id, email: res.data.email, username: res.data.username, role: res.data.role, avatar_url: res.data.avatar_url });
        queryClient.invalidateQueries({ queryKey: ['profile'] });
      }
    },
  });

  const onSubmit = (data: TProfileForm) => {
    const payload: IUserUpdateRequest = {};
    if (data.username) payload.username = data.username;
    if (data.bio !== undefined) payload.bio = data.bio;
    updateMutation.mutate(payload);
  };

  const handleAvatarChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) avatarMutation.mutate(file);
  };

  if (isLoading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', mt: 8 }}>
        <CircularProgress />
      </Box>
    );
  }

  if (!profile) return null;

  const joinDate = new Date(profile.created_at).toLocaleDateString('en-US', {
    year: 'numeric', month: 'long', day: 'numeric',
  });

  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <Paper elevation={2} sx={{ p: 4 }}>
        <Box sx={{ display: 'flex', alignItems: 'flex-start', gap: 3, mb: 4 }}>
          <Box sx={{ position: 'relative' }}>
            <Avatar
              src={profile.avatar_url ?? undefined}
              sx={{ width: 96, height: 96, fontSize: 32, bgcolor: 'secondary.main' }}
            >
              {profile.username[0].toUpperCase()}
            </Avatar>
            <IconButton
              size="small"
              sx={{
                position: 'absolute',
                bottom: 0,
                right: 0,
                bgcolor: 'background.paper',
                border: '1px solid',
                borderColor: 'divider',
              }}
              onClick={() => fileInputRef.current?.click()}
              disabled={avatarMutation.isPending}
            >
              {avatarMutation.isPending ? <CircularProgress size={14} /> : <CameraAlt fontSize="small" />}
            </IconButton>
            <input
              ref={fileInputRef}
              type="file"
              accept="image/jpeg,image/png,image/gif,image/webp"
              hidden
              onChange={handleAvatarChange}
            />
          </Box>

          <Box sx={{ flexGrow: 1 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
              <Typography variant="h5" fontWeight={700}>{profile.username}</Typography>
              <Chip label={profile.role} size="small" color="primary" variant="outlined" />
            </Box>
            <Typography variant="body2" color="text.secondary">
              Joined {joinDate}
            </Typography>
          </Box>

          <Button
            startIcon={<Edit />}
            variant="outlined"
            onClick={() => setIsEditing((v) => !v)}
          >
            {isEditing ? 'Cancel' : 'Edit'}
          </Button>
        </Box>

        <Divider sx={{ mb: 3 }} />

        <Grid container spacing={3} sx={{ mb: 3 }}>
          <Grid item xs={6} sm={3}>
            <Typography variant="h5" fontWeight={700} align="center">{profile.post_count}</Typography>
            <Typography variant="caption" color="text.secondary" align="center" display="block">Posts</Typography>
          </Grid>
          <Grid item xs={6} sm={3}>
            <Typography variant="h5" fontWeight={700} align="center">0</Typography>
            <Typography variant="caption" color="text.secondary" align="center" display="block">Answers</Typography>
          </Grid>
        </Grid>

        {isEditing ? (
          <Box component="form" onSubmit={handleSubmit(onSubmit)}>
            <TextField
              fullWidth
              label="Username"
              margin="normal"
              error={!!errors.username}
              helperText={errors.username?.message}
              {...register('username')}
            />
            <TextField
              fullWidth
              label="Bio"
              margin="normal"
              multiline
              rows={3}
              error={!!errors.bio}
              helperText={errors.bio?.message}
              {...register('bio')}
            />
            <Button
              type="submit"
              variant="contained"
              sx={{ mt: 2 }}
              disabled={updateMutation.isPending}
            >
              {updateMutation.isPending ? <CircularProgress size={20} /> : 'Save Changes'}
            </Button>
          </Box>
        ) : (
          <Box>
            <Typography variant="subtitle2" color="text.secondary" gutterBottom>Email</Typography>
            <Typography gutterBottom>{profile.email}</Typography>
            {profile.bio && (
              <>
                <Typography variant="subtitle2" color="text.secondary" gutterBottom sx={{ mt: 2 }}>Bio</Typography>
                <Typography>{profile.bio}</Typography>
              </>
            )}
          </Box>
        )}
      </Paper>
    </Container>
  );
};

export default ProfilePage;
