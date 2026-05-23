// purpose: Service with business logic + interfaces
// consumes: See content/02-output-contract.xml inputs
// produces: artefact conforming to content/02-output-contract.xml
// depends-on: content/01-core-rules.xml
// token-budget-impact: ~200-1000 tokens when loaded as context
import { User } from '@prisma/client';
import { IUserRepository } from './user-repository';
import { NotFoundError, ConflictError, UnauthorizedError } from './errors';
import { hashPassword, comparePasswords } from '../utils/password';

interface CreateUserDto { email: string; name: string; password: string }
interface UpdateUserDto { email?: string; name?: string }
interface PaginatedUsers { users: User[]; total: number; page: number; limit: number; pages: number }

export class UserService {
  constructor(private userRepository: IUserRepository) {}

  async getUser(id: string): Promise<User> {
    const user = await this.userRepository.findById(id);
    if (!user) throw new NotFoundError(`User ${id} not found`);
    return user;
  }

  async getUsers(page: number, limit: number, search?: string): Promise<PaginatedUsers> {
    const { users, total } = await this.userRepository.findAll({ page, limit, search });
    return { users, total, page, limit, pages: Math.ceil(total / limit) };
  }

  async createUser(data: CreateUserDto): Promise<User> {
    const existing = await this.userRepository.findByEmail(data.email);
    if (existing) throw new ConflictError('User with this email already exists');
    const hashedPassword = await hashPassword(data.password);
    return this.userRepository.create({ email: data.email, name: data.name, hashedPassword });
  }

  async updateUser(id: string, data: UpdateUserDto): Promise<User> {
    await this.getUser(id);
    if (data.email) {
      const existing = await this.userRepository.findByEmail(data.email);
      if (existing && existing.id !== id) throw new ConflictError('Email already in use');
    }
    return this.userRepository.update(id, data);
  }

  async deleteUser(id: string): Promise<void> {
    await this.getUser(id);
    await this.userRepository.delete(id);
  }

  async authenticateUser(email: string, password: string): Promise<User> {
    const user = await this.userRepository.findByEmail(email);
    if (!user) throw new UnauthorizedError('Invalid credentials');
    const valid = await comparePasswords(password, user.hashedPassword);
    if (!valid) throw new UnauthorizedError('Invalid credentials');
    return user;
  }
}
