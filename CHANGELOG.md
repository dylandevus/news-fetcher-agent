## [0.1.0] - 2025-04-16

### Added
- Configuration file for `LocalLLaMA` and `ChatGPTPro`.
- Navigation support using `useKeyNav` in the posts list.
- Functionality to show upvotes and link to comments in `PostContent`.
- New `Post` and `SourceEnum` types for better type management.
- Utility functions for fetching Reddit top posts and YAML data.

### Changed
- Refactored naming from `news` to `posts` across the codebase, including database and model updates.
- Improved styling for post list and content components.
- Enhanced key navigation for the posts list.

### Fixed
- Resolved linting issues in the codebase.
- Corrected imports and ensured proper display of subreddit information and upvotes.
- Fixed minor issues in the `reddit_react.yaml` configuration.

### Removed
- Removed obsolete `postcss.config.js` file from the UI directory.