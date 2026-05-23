// purpose: Controller with decode + service call + encode
// consumes: See content/02-output-contract.xml inputs
// produces: artefact conforming to content/02-output-contract.xml
// depends-on: content/01-core-rules.xml
// token-budget-impact: ~200-1000 tokens when loaded as context
import { Request, Response, NextFunction } from 'express';
import { UserService } from './user-service';
import { CreateUserSchema, UpdateUserSchema } from '../schemas/users';

export class UserController {
  constructor(private userService: UserService) {}

  getUsers = async (req: Request, res: Response, next: NextFunction): Promise<void> => {
    try {
      const page = parseInt(req.query.page as string) || 1;
      const limit = parseInt(req.query.limit as string) || 20;
      const search = req.query.search as string | undefined;
      res.json(await this.userService.getUsers(page, limit, search));
    } catch (error) { next(error); }
  };

  getUser = async (req: Request, res: Response, next: NextFunction): Promise<void> => {
    try {
      res.json({ data: await this.userService.getUser(req.params.id) });
    } catch (error) { next(error); }
  };

  createUser = async (req: Request, res: Response, next: NextFunction): Promise<void> => {
    try {
      const data = CreateUserSchema.parse(req.body);
      res.status(201).json({ data: await this.userService.createUser(data) });
    } catch (error) { next(error); }
  };

  updateUser = async (req: Request, res: Response, next: NextFunction): Promise<void> => {
    try {
      const data = UpdateUserSchema.parse(req.body);
      res.json({ data: await this.userService.updateUser(req.params.id, data) });
    } catch (error) { next(error); }
  };

  deleteUser = async (req: Request, res: Response, next: NextFunction): Promise<void> => {
    try {
      await this.userService.deleteUser(req.params.id);
      res.status(204).send();
    } catch (error) { next(error); }
  };
}
