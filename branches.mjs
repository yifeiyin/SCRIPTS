await $`git fetch --all --prune`

const branchesRaw = (await $`git branch --list --remotes`).toString().split('\n').map(br => br.trim()).filter(br => br !== '');
const branches = branchesRaw.flatMap(br => br.startsWith('origin/HEAD -> origin/') ? [] : br.replace('origin/', ''))

// const branches = ['main', 'dev', 'v3.23', 'pnp-main', 'pnp-dev', 'automerge-main-dev', 'oht-delete-tags'];

branches.sort();

const sectionMatchers = {
  'main-or-dev': /^(main|dev)$/,
  'dash-dev-only': /-dev$/,
  'dash-main-only': /-main$/,
  'v3.xx': /^v3\./,
  'auto-merge': /automerge/,
  'dependabot': /^dependabot\//,
  'SD': /(SD|sd)-/,
  'others': /.*/,
}

const sections = {
  'dash-dev-and-main': [],
};

Object.keys(sectionMatchers).forEach(section => { sections[section] = [] });

branches.forEach(br => {
  for (const section in sectionMatchers) {
    if (sectionMatchers[section].test(br)) {
      sections[section].push(br);
      return;
    }
  }
});

sections['dash-dev-only'] = sections['dash-dev-only'].flatMap(br => {
  const mainBr = br.replace(/-dev$/, '-main')
  if (sections['dash-main-only'].includes(mainBr)) {
    sections['dash-dev-and-main'].push(br)
    sections['dash-dev-and-main'].push(mainBr)
    sections['dash-main-only'].splice(sections['dash-main-only'].indexOf(mainBr), 1)
    return [];
  }
  return br;
});

/**
 * Get last commit timestamp for each branch
 */
const timestampMap = {};
await Promise.all(branches.map(async (br) => {
  const timestamp = (await $`git show --no-patch --pretty=format:%ct ${'origin/' + br}`).toString();
  timestampMap[br] = dateToRelativeInWeeks(Number(timestamp));
}));

const repoRootURL = (await $`gh repo view --json 'url' --jq '.url'`).toString().trim();

/**
 * Get closest branch and distance for each branch
 */
const baseBranches = [...sections['dash-dev-and-main'], sections['main-or-dev']].filter(x => x.includes('dev'));
const closestBranchMap = {};
// await Promise.all(branches.map(async (br) => {
//   if (sections['SD'].includes(br) || sections['others'].includes(br)) {
//     const closestBranch = await getClosestBranch(baseBranches, br);
//     closestBranchMap[br] = closestBranch.distance + ',' + closestBranch.branch + ',' + findPR(repoRootURL, br, closestBranch.branch);
//   }
// }));

// Use for loop instead
for (const br of [...sections['SD'], ...sections['others']]) {
  const closestBranch = await getClosestBranch(baseBranches, br);
  closestBranchMap[br] = closestBranch.distance + ',' + closestBranch.branch + ',' + findPR(repoRootURL, br, closestBranch.branch);
}

/**
 * Generate Output
 */
const outputLines = [];
for (const section in sections) {
  outputLines.push(`~~~~~~~~ ${section} ~~~~~~~~`);
  sections[section].forEach(br => {
    outputLines.push(`${br},${timestampMap[br]},${closestBranchMap[br] || ''}`);
  })
  outputLines.push('');
}
console.log(outputLines.join('\n'));


async function getClosestBranch(possibleBranches, branch) {
  const distanceToBranches = await Promise.all(possibleBranches.map(async (possibleMatch) => {
    const result = await $`git rev-list --count ^origin/${possibleMatch} origin/${branch}`;
    if (result.exitCode !== 0) {
      throw new Error(result.stderr.toString());
    }
    return { distance: Number(result.stdout.toString()), branch: possibleMatch };
  }))

  const closestDistanceAndBranch = distanceToBranches.sort((a, b) => a.distance - b.distance)[0];
  return closestDistanceAndBranch;
}

function findPR(repoBaseURL, fromBranch, toBranch) {
  return `${repoBaseURL}/compare/${toBranch}...${fromBranch}`
}

function dateToRelativeInWeeks(tsInSeconds) {
  let out = (new Date() - new Date(tsInSeconds * 1000)) / 1000 / 60 / 60 / 24 / 7;
  out = Math.round(out * 10) / 10;
  return out === 1 ? '1 week ago' : (out + ' weeks ago');
}

