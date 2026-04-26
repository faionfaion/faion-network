import { EntityBuilder } from './entity-builder';

// Pattern: Object Mother returns Builder so callers can further customize
// Usage: UserMother.admin().withEmail('custom@test.com').build()

export class UserMother {
  static admin(): EntityBuilder {
    return new EntityBuilder()
      .withName('Admin User')
      .withEmail('admin@example.com')
      .asActive()
      .withMetadata({ role: 'admin' });
  }

  static regular(): EntityBuilder {
    return new EntityBuilder()
      .withName('Regular User')
      .withEmail('user@example.com')
      .asActive()
      .withMetadata({ role: 'member' });
  }

  static guest(): EntityBuilder {
    return new EntityBuilder()
      .withName('Guest User')
      .withEmail('guest@example.com')
      .withStatus('pending')
      .withMetadata({ role: 'guest', verified: false });
  }

  static inactive(): EntityBuilder {
    return new EntityBuilder()
      .withName('Inactive User')
      .withEmail('inactive@example.com')
      .asInactive();
  }
}
