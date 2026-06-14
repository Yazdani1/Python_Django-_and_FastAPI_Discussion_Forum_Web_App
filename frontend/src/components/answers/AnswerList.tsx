import { type FC } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { Box, CircularProgress, Divider, Typography } from '@mui/material';
import { answerService } from '@/services/answerService';
import { voteService } from '@/services/voteService';
import { useAuth } from '@/hooks/useAuth';
import { AnswerCard } from './AnswerCard';
import { AnswerForm, type TAnswerFormValues } from './AnswerForm';

interface IAnswerListProps {
  postId: string;
}

export const AnswerList: FC<IAnswerListProps> = ({ postId }) => {
  const { user } = useAuth();
  const queryClient = useQueryClient();

  const { data: res, isLoading } = useQuery({
    queryKey: ['answers', postId],
    queryFn: () => answerService.listAnswers(postId),
  });

  const addMutation = useMutation({
    mutationFn: (data: TAnswerFormValues) => answerService.addAnswer(postId, data),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['answers', postId] }),
  });

  const deleteMutation = useMutation({
    mutationFn: (answerId: string) => answerService.deleteAnswer(answerId),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['answers', postId] }),
  });

  const updateMutation = useMutation({
    mutationFn: ({ answerId, content }: { answerId: string; content: string }) =>
      answerService.updateAnswer(answerId, { content }),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['answers', postId] }),
  });

  const voteMutation = useMutation({
    mutationFn: (answerId: string) => voteService.voteAnswer(answerId, { vote_type: 'up' }),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['answers', postId] }),
  });

  const answers = res?.data ?? [];

  const handleAdd = async (data: TAnswerFormValues) => {
    await addMutation.mutateAsync(data);
  };

  const handleUpdate = async (answerId: string, content: string) => {
    await updateMutation.mutateAsync({ answerId, content });
  };

  return (
    <Box sx={{ mt: 4 }}>
      <Divider sx={{ mb: 3 }} />
      <Typography variant="h6" fontWeight={600} gutterBottom>
        {answers.length} {answers.length === 1 ? 'Answer' : 'Answers'}
      </Typography>

      {isLoading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', py: 4 }}>
          <CircularProgress />
        </Box>
      ) : (
        <Box>
          {answers.map((answer) => (
            <AnswerCard
              key={answer.id}
              answer={answer}
              currentUserId={user?.id ?? null}
              currentUserRole={user?.role ?? null}
              onDelete={(id) => deleteMutation.mutate(id)}
              onUpdate={handleUpdate}
              onVote={(id) => voteMutation.mutate(id)}
              isVoteLoading={voteMutation.isPending}
            />
          ))}
        </Box>
      )}

      {user ? (
        <Box sx={{ mt: 3 }}>
          <Typography variant="subtitle1" fontWeight={600} gutterBottom>
            Your Answer
          </Typography>
          <AnswerForm onSubmit={handleAdd} isSubmitting={addMutation.isPending} />
        </Box>
      ) : (
        <Box sx={{ mt: 3, p: 2, bgcolor: 'action.hover', borderRadius: 1 }}>
          <Typography variant="body2" color="text.secondary">
            Log in to post an answer.
          </Typography>
        </Box>
      )}
    </Box>
  );
};
