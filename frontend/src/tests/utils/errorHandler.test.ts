import { describe, it, expect } from 'vitest';
import axios from 'axios';
import { handleError } from '@/utils/errorHandler';

describe('handleError', () => {
  it('returns parsed message for a plain Error', () => {
    const result = handleError(new Error('Something went wrong'));
    expect(result.message).toBe('Something went wrong');
    expect(result.errors).toEqual([]);
    expect(result.statusCode).toBe(0);
  });

  it('returns custom message when provided for a plain Error', () => {
    const result = handleError(new Error('original'), 'Custom message');
    expect(result.message).toBe('Custom message');
  });

  it('returns fallback for unknown error', () => {
    const result = handleError('some string error');
    expect(result.message).toBe('An unexpected error occurred.');
    expect(result.statusCode).toBe(0);
  });

  it('returns custom message for unknown error when provided', () => {
    const result = handleError(null, 'Override message');
    expect(result.message).toBe('Override message');
  });

  it('uses default 401 message for axios 401 error without body', () => {
    const error = new axios.AxiosError('Unauthorized');
    error.response = {
      status: 401,
      data: undefined,
      headers: {},
      config: {} as never,
      statusText: 'Unauthorized',
    };
    const result = handleError(error);
    expect(result.statusCode).toBe(401);
    expect(result.message).toContain('session');
  });

  it('uses API response message when present in axios error', () => {
    const error = new axios.AxiosError('Bad Request');
    error.response = {
      status: 400,
      data: { success: false, message: 'Email already taken', data: null, errors: null, meta: null },
      headers: {},
      config: {} as never,
      statusText: 'Bad Request',
    };
    const result = handleError(error);
    expect(result.message).toBe('Email already taken');
    expect(result.statusCode).toBe(400);
  });
});
