// src/container.ts — Single source of truth for DI wiring.
// Prisma must be module-level singleton — never inside a function.
// Feature agents: read this file before adding new constructor injections.

import { PrismaClient } from '@prisma/client';
import { UserRepository } from './repositories/users.repository';
import { UserService } from './services/users.service';
import { UserController } from './controllers/users.controller';
// Add additional imports here as new entities are added

const prisma = new PrismaClient();

const userRepository = new UserRepository(prisma);
const userService = new UserService(userRepository);
const userController = new UserController(userService);

export { prisma, userRepository, userService, userController };
