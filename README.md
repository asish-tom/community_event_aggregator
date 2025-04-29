[Previous README content up to Contributing section...]

## Contributing

### Pull Request Process

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Ensure tests pass with coverage requirements (`pytest --cov=src`)
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Create a Pull Request

### Merge Queue Process

The project uses GitHub's merge queue to ensure safe and automated merging of pull requests.

1. Prerequisites for merging:
   - All required checks must pass
   - Code coverage must be ≥ 90%
   - At least one approval from maintainers
   - No merge conflicts

2. Getting your PR merged:
   - Add the `ready-to-merge` label to your PR
   - PR will be automatically added to the merge queue
   - Queue will run validation checks
   - PR will be merged when all checks pass

3. Branch Protection Rules:
   - Direct pushes to main are blocked
   - PRs require review approval
   - Status checks must pass
   - Merge queue is required

### Setting up Merge Queue (for maintainers)

1. Enable branch protection:
   - Go to repository Settings > Branches
   - Add rule for `main` branch
   - Enable "Require a pull request before merging"
   - Enable "Require status checks to pass"
   - Enable "Require merge queue"

2. Configure merge queue:
   - Check "Require branches to be up to date"
   - Set minimum number of approvals
   - Enable "Dismiss stale pull request approvals"
   - Enable "Require review from Code Owners"

3. Queue settings:
   - Maximum batch size: 5
   - Minimum time in queue: 10 minutes
   - Required checks:
     - Tests workflow
     - Coverage validation
     - Merge queue validation

[Rest of README content...]