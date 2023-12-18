/*
Usage: zx cherry-pick.mjs

Dependencies:
- [zx](https://github.com/google/zx)
- [gh](https://cli.github.com)
*/

const BRANCH_PREFIX = 'sonarqube'
const PR_TITLE = 'Add SonarQube github action to ' // + branch name
const COMMIT_HASH = await question('Commit hash: ')

const branches = (await question('Branch names, whitespace-separated: ')).split(/\s+/).filter(Boolean)

const linksToPRs = [];

try {
  await $`git fetch --all --prune`
} catch (error) {
  console.error(error);
  process.exit()
}

for (const branch of branches) {
  const newBranchName = `${BRANCH_PREFIX}-${branch}-cherry-pick-${COMMIT_HASH}`
  try {
    await $`git checkout --quiet ${branch}`
    await $`git pull`
    await $`git checkout --quiet -b ${newBranchName}`
    await $`git cherry-pick ${COMMIT_HASH}`
    await $`git push --quiet -u origin ${newBranchName}`

    const link = await $`gh pr create --head ${newBranchName} --base ${branch} --title ${PR_TITLE + branch} --body "Cherry-picking ${COMMIT_HASH} to ${branch}."`
    linksToPRs.push(link.toString().trim());

    // await question('Continue?')

  } catch (error) {
    console.error(error);
    process.exit();
  }
}

console.log('Script completed. Links to PRs:');
console.log(linksToPRs.join('\n'));
