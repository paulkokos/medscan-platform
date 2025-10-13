# GitHub Projects Setup

This document describes the GitHub Projects setup for the MedScan Platform.

## Project Structure

The MedScan Platform uses GitHub Projects (beta) to track development progress across multiple areas:

### Project Board: MedScan Development

**Views:**

1. **Backlog** - All open issues not yet assigned to a sprint
2. **Current Sprint** - Active work items for the current development cycle
3. **In Progress** - Issues currently being worked on
4. **In Review** - Pull requests and issues awaiting review
5. **Done** - Completed issues

**Custom Fields:**

- **Priority**: High, Medium, Low
- **Component**: Backend, Frontend, DevOps, Documentation
- **Sprint**: Sprint number (e.g., Sprint 1, Sprint 2)
- **Estimate**: Story points (1, 2, 3, 5, 8, 13)
- **Status**: Backlog, Todo, In Progress, In Review, Done

## How to Use

### Adding Issues to the Project

1. Create an issue using one of the templates
2. The issue will automatically be added to the project backlog
3. Assign labels, priority, and component
4. Move to appropriate column based on status

### Sprint Planning

1. Review backlog items
2. Assign issues to current sprint using the Sprint field
3. Move issues from Backlog to Current Sprint view
4. Assign team members to issues

### Updating Status

- Move cards between columns as work progresses
- Update status field when:
  - Starting work (Backlog ’ In Progress)
  - Opening PR (In Progress ’ In Review)
  - Merging PR (In Review ’ Done)

### Automation

The project board has automation rules:

- Issues with linked PRs automatically move to "In Review"
- Closed issues automatically move to "Done"
- Issues with "blocked" label are highlighted

## Best Practices

1. Keep issue titles clear and concise
2. Use estimates for planning capacity
3. Add detailed descriptions with acceptance criteria
4. Link related issues and PRs
5. Update status regularly
6. Review and groom backlog weekly

## Views

### Developer View
Filtered by assignee, showing only your assigned issues

### Component View
Grouped by component (Backend/Frontend/DevOps)

### Priority View
Sorted by priority, showing high-priority items first

## Resources

- [GitHub Projects Documentation](https://docs.github.com/en/issues/planning-and-tracking-with-projects)
- [Project Board](../../projects)
