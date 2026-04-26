# RSpec model spec skeleton
# Replace: User, :user factory, field names, association names

require 'rails_helper'

RSpec.describe User, type: :model do
  # --- Validations (shoulda-matchers) ---
  describe 'validations' do
    it { is_expected.to validate_presence_of(:email) }
    it { is_expected.to validate_presence_of(:name) }
    it { is_expected.to validate_uniqueness_of(:email).case_insensitive }
    it { is_expected.to validate_length_of(:name).is_at_least(2).is_at_most(100) }
  end

  # --- Associations ---
  describe 'associations' do
    it { is_expected.to belong_to(:organization) }
    it { is_expected.to have_many(:orders).dependent(:nullify) }
    it { is_expected.to have_one(:profile).dependent(:destroy) }
  end

  # --- Scopes ---
  describe '.active' do
    let!(:active_user)   { create(:user, active: true) }
    let!(:inactive_user) { create(:user, active: false) }

    it 'returns only active users' do
      expect(described_class.active).to contain_exactly(active_user)
    end
  end

  # --- Instance methods (no DB write needed) ---
  describe '#full_name' do
    let(:user) { build(:user, first_name: 'John', last_name: 'Doe') }

    it 'combines first and last name' do
      expect(user.full_name).to eq('John Doe')
    end
  end
end
