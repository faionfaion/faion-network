// app/<route>/actions.ts — Server Action with Zod validation, revalidatePath, redirect
'use server';

import { revalidatePath } from 'next/cache';
import { redirect } from 'next/navigation';
import { z } from 'zod';
import { db } from '@/lib/db';

const CreatePostSchema = z.object({
  title: z.string().min(1).max(100),
  content: z.string().min(1),
});

export async function createPost(formData: FormData) {
  const parsed = CreatePostSchema.safeParse({
    title: formData.get('title'),
    content: formData.get('content'),
  });

  if (!parsed.success) {
    return { error: parsed.error.flatten() };
  }

  const post = await db.post.create({
    data: parsed.data,
  });

  revalidatePath('/posts');
  redirect(`/posts/${post.id}`); // NOT inside try/catch
}
