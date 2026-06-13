import { type FC } from 'react';
import { zodResolver } from '@hookform/resolvers/zod';
import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { Box, Button, CircularProgress, TextField } from '@mui/material';

const postSchema = z.object({
  title: z.string().min(5, 'Title must be at least 5 characters').max(200, 'Title is too long'),
  content: z.string().min(10, 'Content must be at least 10 characters'),
});

export type TPostFormValues = z.infer<typeof postSchema>;

interface IPostFormProps {
  defaultValues?: Partial<TPostFormValues>;
  onSubmit: (data: TPostFormValues) => Promise<void>;
  submitLabel?: string;
  isSubmitting?: boolean;
}

export const PostForm: FC<IPostFormProps> = ({
  defaultValues,
  onSubmit,
  submitLabel = 'Submit',
  isSubmitting = false,
}) => {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<TPostFormValues>({
    resolver: zodResolver(postSchema),
    defaultValues,
  });

  return (
    <Box component="form" onSubmit={handleSubmit(onSubmit)} noValidate>
      <TextField
        fullWidth
        label="Title"
        margin="normal"
        error={!!errors.title}
        helperText={errors.title?.message}
        {...register('title')}
      />

      <TextField
        fullWidth
        label="Content"
        margin="normal"
        multiline
        rows={8}
        error={!!errors.content}
        helperText={errors.content?.message}
        {...register('content')}
      />

      <Button
        type="submit"
        variant="contained"
        size="large"
        disabled={isSubmitting}
        sx={{ mt: 2 }}
      >
        {isSubmitting ? <CircularProgress size={24} /> : submitLabel}
      </Button>
    </Box>
  );
};
