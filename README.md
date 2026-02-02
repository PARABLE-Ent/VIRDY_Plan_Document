# VIRDY Plan Document

> Comprehensive planning and design documentation for the VIRDY Solution

This repository serves as the centralized documentation hub for VIRDY's product planning, technical design, and operational strategies. It provides structured specifications across all phases of product development.

## Overview

VIRDY is an all-in-one motion capture live streaming solution for virtual creators. This repository contains the complete planning documentation organized into five primary categories:

- **Product**: Core product definition and user flows
- **Features**: Detailed specifications for key features
- **Operations**: User management, licensing, and security policies
- **Design**: UI/UX specifications and design guidelines
- **Technical**: System architecture and development status

## Repository Structure

```
VIRDY_Plan_Document/
├── 01_Product/
│   ├── 01_Product_Overview.md
│   └── 02_User_Flow.md
├── 02_Features/
│   ├── 01_Avatar_System.md
│   ├── 02_Tracker_System.md
│   ├── 03_Camera_System.md
│   ├── 04_World_System.md
│   ├── 05_Network_System.md
│   └── 06_SDK.md
├── 03_Operations/
│   ├── 01_User_Roles.md
│   ├── 02_License_System.md
│   ├── 03_Security.md
│   ├── 04_Data_Lifecycle.md
│   ├── 05_Risk_Management.md
│   └── 06_Account_System.md
├── 04_Design/
│   └── 01_UI_Specification.md
└── 05_Technical/
    ├── 01_Architecture.md
    └── 02_Development_Status.md
```

## Quick Start

### Viewing Documentation

**Option 1: HTML Viewer (Recommended)**

Open `VIRDY_Onboarding.html` in your browser for an integrated view with navigation sidebar and search functionality.

```bash
# Open the HTML file
start VIRDY_Onboarding.html  # Windows
open VIRDY_Onboarding.html   # macOS
xdg-open VIRDY_Onboarding.html  # Linux
```

**Option 2: Markdown Files**

Navigate through individual `.md` files organized by category in their respective folders.

**Option 3: Notion**

Documentation is synchronized with VIRDY Notion workspace for collaborative editing and comments.

## Documentation Categories

### 01_Product
Product vision, target users, and core value propositions. Includes complete user journey flows from authentication to production.

### 02_Features
Technical specifications for:
- Avatar system (VRM support, BlendShape configuration)
- Tracker integration (14+ device types)
- Camera system (10-channel virtual cameras)
- World management (AssetBundle, sharing policies)
- Network synchronization (Photon Fusion 2)
- SDK for custom content creation

### 03_Operations
Operational policies covering:
- User role definitions (Creator vs Manager)
- SaaS licensing tiers (Free/Pro/Studio/Enterprise)
- Security protocols and data protection
- Session lifecycle management
- Risk mitigation strategies
- Account system architecture

### 04_Design
UI/UX specifications and design system guidelines.

### 05_Technical
System architecture documentation and current development status tracking.

## Document Format

All planning documents follow a standardized structure:

```markdown
# Document Title

> **Document Version**: X.X
> **Last Updated**: YY.MM.DD HH:MM
> **Author**: Name

## 1. Overview
## 2. Core Specifications
## 3. Design Considerations
## 4. Edge Cases and Exception Handling
## 5. Future Extensibility
```

## Contributing

This repository is maintained by VIRDY Studio. For contributions or suggestions:

1. Check existing documentation for context
2. Follow the established document format
3. Ensure changes are reflected in both local `.md` files and Notion workspace
4. Update `VIRDY_Onboarding.html` by running `generate_onboarding.py`

## Generating HTML Documentation

To regenerate the integrated HTML documentation:

```bash
cd VIRDY_Plan_Document
python generate_onboarding.py
```

This creates `VIRDY_Onboarding.html` with all documents integrated into a single-page viewer.

## Related Resources

- **VIRDY Framework**: [Unity client repository](https://github.com/PARABLE-Ent/VIRDY-Framework-Dev)
- **VIRDY Docs**: [Official documentation site](https://parable-ent.github.io/VIRDY-Docs/)
- **Notion Workspace**: VIRDY Planning (internal)

## License

Copyright © 2026 VIRDY Studio. All rights reserved.

---

**Maintained by**: VIRDY Studio
**For inquiries**: Contact through official channels
