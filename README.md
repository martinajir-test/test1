# test1

A test repository.

## Development Setup

This guide walks you through getting the project running locally for development.

### Prerequisites

Before you begin, ensure you have the following installed on your machine:

- **Git** (v2.x or later) — [Download](https://git-scm.com/downloads)
- **Node.js** (v20 or later) — [Download](https://nodejs.org/) or use a version manager such as [nvm](https://github.com/nvm-sh/nvm)
- **npm** (v10 or later, included with Node.js)

Verify your installations:

```bash
git --version
node --version
npm --version
```

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/martinajir-test/test1.git
   cd test1
   ```

2. **Install dependencies**

   ```bash
   npm install
   ```

3. **Set up environment variables** (if applicable)

   Copy the example environment file and fill in the required values:

   ```bash
   cp .env.example .env
   ```

   Edit `.env` with your local configuration.

### Common Development Commands

| Command | Description |
|---------|-------------|
| `npm run dev` | Start the development server with hot-reload |
| `npm run build` | Build the project for production |
| `npm test` | Run the test suite |
| `npm run lint` | Run the linter to check for code style issues |
| `npm run lint:fix` | Run the linter and automatically fix fixable issues |
| `npm run format` | Format source files with Prettier |

### Running Tests

```bash
# Run all tests
npm test

# Run tests in watch mode
npm run test:watch

# Run tests with coverage report
npm run test:coverage
```

### Contributing

1. Create a new branch from `main`:

   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and commit them with a descriptive message.

3. Push your branch and open a pull request against `main`.
