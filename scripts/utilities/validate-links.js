/**
 * Script to validate internal links in documentation
 * This is a placeholder script - in a real implementation, it would validate links
 */

const fs = require('fs');
const path = require('path');

function findMarkdownFiles(dir) {
    let results = [];
    const items = fs.readdirSync(dir);

    for (const item of items) {
        const fullPath = path.join(dir, item);
        const stat = fs.statSync(fullPath);

        if (stat.isDirectory()) {
            results = results.concat(findMarkdownFiles(fullPath));
        } else if (path.extname(fullPath) === '.md') {
            results.push(fullPath);
        }
    }

    return results;
}

function validateLinks(docsDir) {
    console.log('Starting link validation...');

    // Find all markdown files in the docs directory
    const markdownFiles = findMarkdownFiles(docsDir);

    console.log(`Found ${markdownFiles.length} markdown files to validate`);

    let totalIssues = 0;

    for (const file of markdownFiles) {
        const content = fs.readFileSync(file, 'utf8');

        // Simple regex to find markdown links
        const linkRegex = /\[([^\]]+)\]\(([^)]+)\)/g;
        let match;

        while ((match = linkRegex.exec(content)) !== null) {
            const [fullMatch, linkText, linkUrl] = match;

            // Check if it's an internal link (doesn't start with http)
            if (!linkUrl.startsWith('http') && !linkUrl.startsWith('#')) {
                // Check if the file exists
                const linkPath = path.resolve(path.dirname(file), linkUrl);

                // For relative links that should point to other docs
                if (!fs.existsSync(linkPath)) {
                    console.log(`⚠️  Potential broken link in ${file}: ${linkUrl}`);
                    totalIssues++;
                }
            }
        }
    }

    console.log(`\nLink validation complete!`);
    console.log(`Found ${totalIssues} potential issues`);

    return totalIssues === 0;
}

// If running this script directly
if (require.main === module) {
    const docsDir = path.join(__dirname, '..', '..', 'frontend', 'docs');

    if (!fs.existsSync(docsDir)) {
        console.error(`Error: Docs directory not found at ${docsDir}`);
        process.exit(1);
    }

    const isValid = validateLinks(docsDir);

    if (!isValid) {
        console.log('Some links may be broken. Please review the warnings above.');
        process.exit(1);
    } else {
        console.log('All links appear to be valid!');
        process.exit(0);
    }
}

module.exports = { validateLinks };