import { describe, it, expect, vi, beforeEach } from 'vitest';

vi.mock('notistack', () => ({
  enqueueSnackbar: vi.fn(),
}));

import { enqueueSnackbar } from 'notistack';
import { notificationService } from '@/utils/notificationService';

describe('notificationService', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('calls enqueueSnackbar with success variant', () => {
    notificationService.success('Done!');
    expect(enqueueSnackbar).toHaveBeenCalledWith('Done!', { variant: 'success' });
  });

  it('calls enqueueSnackbar with error variant', () => {
    notificationService.error('Failed!');
    expect(enqueueSnackbar).toHaveBeenCalledWith('Failed!', { variant: 'error' });
  });

  it('calls enqueueSnackbar with warning variant', () => {
    notificationService.warning('Careful!');
    expect(enqueueSnackbar).toHaveBeenCalledWith('Careful!', { variant: 'warning' });
  });

  it('calls enqueueSnackbar with info variant', () => {
    notificationService.info('FYI');
    expect(enqueueSnackbar).toHaveBeenCalledWith('FYI', { variant: 'info' });
  });
});
