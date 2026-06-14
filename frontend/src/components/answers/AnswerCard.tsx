import { useState, type FC } from 'react';
import { Avatar, Box, Divider, Typography } from '@mui/material';
import { Delete, Edit } from '@mui/icons-material';
import type { TUserRole } from '@/types/auth.types';
import type { IAnswer } from '@/types/answer.types';
import { VoteButtons } from '@/components/posts/VoteButtons';
import { ActionsMenu } from '@/components/common/ActionsMenu';
import { AnswerForm, type TAnswerFormValues } from './AnswerForm';

interface IAnswerCardProps {
  answer: IAnswer;
  currentUserId: string | null;
  currentUserRole: TUserRole | null;
  onDelete: (answerId: string) => void;
  onUpdate: (answerId: string, content: string) => Promise<void>;
  onVote: (answerId: string) => void;
  isVoteLoading?: boolean;
}

export const AnswerCard: FC<IAnswerCardProps> = ({
  answer,
  currentUserId,
  currentUserRole,
  onDelete,
  onUpdate,
  onVote,
  isVoteLoading = false,
}) => {
  const [editing, setEditing] = useState(false);
  const [isUpdating, setIsUpdating] = useState(false);

  const isOwner = currentUserId === answer.author.id;
  const isPrivileged = currentUserRole === 'moderator' || currentUserRole === 'admin';
  const canManage = isOwner || isPrivileged;

  const formattedDate = new Date(answer.created_at).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  });

  const handleUpdate = async (data: TAnswerFormValues) => {
    setIsUpdating(true);
    try {
      await onUpdate(answer.id, data.content);
      setEditing(false);
    } finally {
      setIsUpdating(false);
    }
  };

  return (
    <Box>
      <Box sx={{ display: 'flex', gap: 2, py: 2 }}>
        <Avatar
          src={answer.author.avatar_url ?? undefined}
          sx={{ width: 36, height: 36, bgcolor: 'secondary.main', fontSize: 15, flexShrink: 0 }}
        >
          {answer.author.username[0].toUpperCase()}
        </Avatar>

        <Box sx={{ flexGrow: 1 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 0.5 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <Typography variant="body2" fontWeight={600}>
                {answer.author.username}
              </Typography>
              <Typography variant="caption" color="text.disabled">
                {formattedDate}
              </Typography>
            </Box>

            {canManage && !editing && (
              <ActionsMenu
                items={[
                  ...(isOwner
                    ? [{
                        label: 'Edit',
                        icon: <Edit fontSize="small" />,
                        onClick: () => setEditing(true),
                      }]
                    : []),
                  {
                    label: 'Delete',
                    icon: <Delete fontSize="small" />,
                    onClick: () => onDelete(answer.id),
                    color: 'error' as const,
                  },
                ]}
              />
            )}
          </Box>

          {editing ? (
            <AnswerForm
              defaultValues={{ content: answer.content }}
              onSubmit={handleUpdate}
              onCancel={() => setEditing(false)}
              submitLabel="Save"
              isSubmitting={isUpdating}
            />
          ) : (
            <>
              <Typography variant="body2" sx={{ whiteSpace: 'pre-wrap', lineHeight: 1.7, mb: 1 }}>
                {answer.content}
              </Typography>
              <VoteButtons
                voteCount={answer.vote_count}
                isLiked={answer.user_vote === 'up'}
                onToggle={() => onVote(answer.id)}
                isLoading={isVoteLoading}
                disabled={!currentUserId}
              />
            </>
          )}
        </Box>
      </Box>
      <Divider />
    </Box>
  );
};
