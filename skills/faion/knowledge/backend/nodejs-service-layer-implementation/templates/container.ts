// src/container.ts — Manual DI wiring: Prisma → Repository → Service → Controller
// This file is the single source of truth for all instantiation.
// Feature agents must read this file before adding new constructor injections.

import { PrismaClient } from '@prisma/client';
import { UserRepository } from './repositories/users.repository';
import { UserService } from './services/users.service';
import { UserController } from './controllers/users.controller';

// Singleton database client — must be module-level, never inside a function
const prisma = new PrismaClient();

// Repositories
const userRepository = new UserRepository(prisma);

// Services
const userService = new UserService(userRepository);

// Controllers
const userController = new UserController(userService);

export { prisma, userRepository, userService, userController };
