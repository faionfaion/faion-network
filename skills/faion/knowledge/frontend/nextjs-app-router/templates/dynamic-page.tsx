// app/users/[id]/page.tsx — dynamic page with generateStaticParams and generateMetadata
import { notFound } from 'next/navigation';
import { getUser, getUsers } from '@/lib/queries';

interface PageProps {
  params: Promise<{ id: string }>;
}

// Generate static params for SSG (remove if fully dynamic)
export async function generateStaticParams() {
  const users = await getUsers();
  return users.map((user) => ({ id: user.id }));
}

// Generate metadata dynamically
export async function generateMetadata({ params }: PageProps) {
  const { id } = await params;
  const user = await getUser(id);

  if (!user) {
    return { title: 'User Not Found' };
  }

  return {
    title: user.name,
    description: `Profile of ${user.name}`,
  };
}

export default async function UserPage({ params }: PageProps) {
  const { id } = await params; // Next.js 15: params is a Promise
  const user = await getUser(id);

  if (!user) {
    notFound(); // Do NOT wrap in try/catch
  }

  return (
    <div>
      <h1>{user.name}</h1>
      <p>{user.email}</p>
    </div>
  );
}
