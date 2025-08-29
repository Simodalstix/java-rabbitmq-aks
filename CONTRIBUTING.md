# Contributing

Thanks for your interest in contributing! This project demonstrates cloud-native microservices patterns.

## Development Setup

1. **Fork and clone** the repository
2. **Install prerequisites**: Java 17+, Maven, Docker
3. **Start local environment**: `cd local && docker-compose up -d`
4. **Run tests**: `mvn clean verify`

## Making Changes

1. **Create a feature branch**: `git checkout -b feature/your-feature`
2. **Make your changes** with tests
3. **Ensure CI passes**: All tests and builds must pass
4. **Submit a pull request** with clear description

## Code Standards

- **Java**: Follow Spring Boot conventions
- **Terraform**: Use `terraform fmt` for formatting
- **Commits**: Use conventional commit format (`feat:`, `fix:`, `docs:`)
- **Tests**: Add tests for new functionality

## Infrastructure Changes

- **Test locally** with `terraform plan` before submitting
- **Document cost implications** for new Azure resources
- **Keep it simple** - avoid over-engineering

## Questions?

Open an issue for discussion before major changes.