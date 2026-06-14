import { type FC } from 'react';
import { zodResolver } from '@hookform/resolvers/zod';
import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { Box, Button, CircularProgress, TextField } from '@mui/material';

const answerSchema = z.object({
  content: z.string().min(10, 'Answer must be at least 10 characters'),
});

export type TAnswerFormValues = z.infer<typeof answerSchema>;

interface IAnswerFormProps {
  defaultValues?: Partial<TAnswerFormValues>;
  onSubmit: (data: TAnswerFormValues) => Promise<void>;
  onCancel?: () => void;
  submitLabel?: string;
  isSubmitting?: boolean;
}

export const AnswerForm: FC<IAnswerFormProps> = ({
  defaultValues,
  onSubmit,
  onCancel,
  submitLabel = 'Post Answer',
  isSubmitting = false,
}) => {
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<TAnswerFormValues>({
    resolver: zodResolver(answerSchema),
    defaultValues,
  });

  const handleFormSubmit = async (data: TAnswerFormValues) => {
    await onSubmit(data);
    reset();
  };

  return (
    <Box component="form" onSubmit={handleSubmit(handleFormSubmit)} noValidate>
      <TextField
        fullWidth
        multiline
        rows={4}
        label="Your answer"
        margin="normal"
        error={!!errors.content}
        helperText={errors.content?.message}
        {...register('content')}
      />
      <Box sx={{ display: 'flex', gap: 1, mt: 1 }}>
        <Button type="submit" variant="contained" disabled={isSubmitting}>
          {isSubmitting ? <CircularProgress size={22} /> : submitLabel}
        </Button>
        {onCancel && (
          <Button type="button" variant="outlined" onClick={onCancel}>
            Cancel
          </Button>
        )}
      </Box>
    </Box>
  );
};
