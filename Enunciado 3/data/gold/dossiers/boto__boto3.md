# boto/boto3

Repositório: https://github.com/boto/boto3

## Metadados

- Linguagem: Python

## Releases sorteadas

### Release 1

Link: https://github.com/boto/boto3/releases/tag/0.0.3
- Tag: `0.0.3`
- Nome: Boto 3 - 0.0.3
- Publicada em: 2014-11-26
- Release anterior (cronológica): `0.0.2`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 7

-  Upgrade to newer Travis-CI build hosts.
-  Update requirements to head of develop branches
-  Merge pull request #29 from kyleknap/update-req
-  Blacklist IAM integration test.
-  Update Botocore dependency
-  Bump version to 0.0.3
-  Merge branch 'release-0.0.3'

### Release 2

Link: https://github.com/boto/boto3/releases/tag/0.0.5
- Tag: `0.0.5`
- Nome: Boto 3 - 0.0.5
- Publicada em: 2014-12-16
- Release anterior (cronológica): `0.0.4`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 11

-  Add S3 and SQS integration tests.
-  Update param documentation to be more explicit.
-  Merge pull request #37 from boto/docs-kwargs
-  Default to using us-west-2 for integ tests
-  Merge pull request #36 from boto/integ
-  Fix failing integration test.
-  Implement batch actions.
-  Merge pull request #32 from boto/batch-actions
-  Update Botocore, update changelog
-  Bump version
-  Merge branch 'release-0.0.5'

### Release 3

Link: https://github.com/boto/boto3/releases/tag/0.0.6
- Tag: `0.0.6`
- Nome: Boto 3 - 0.0.6
- Publicada em: 2014-12-18
- Release anterior (cronológica): `0.0.5`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 12

-  Remove the dependency on six module.
-  Merge pull request #42 from boto/remove-six
-  Added waiter actions to resources
-  Add a section for client waiters
-  Touched up the waiter code
-  Merge pull request #43 from kyleknap/waiters
-  Added more docs about waiters
-  Merge pull request #44 from kyleknap/waiter-top-level-docs
-  Update SQS resource model
-  Update changelog
-  Bump version to 0.0.6
-  Merge branch 'release-0.0.6'

### Release 4

Link: https://github.com/boto/boto3/releases/tag/0.0.10
- Tag: `0.0.10`
- Nome: Boto 3 - 0.0.10
- Publicada em: 2015-03-24
- Release anterior (cronológica): `0.0.11`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

_(nenhum commit novo)_

### Release 5

Link: https://github.com/boto/boto3/releases/tag/0.0.14
- Tag: `0.0.14`
- Nome: Boto 3 - 0.0.14
- Publicada em: 2015-04-09
- Release anterior (cronológica): `0.0.13`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 47

-  Merge branch 'release-0.0.12'
-  Initial commit of S3 transfers module
-  Fix multithreaded writes
-  Update docs to reflect latest changes
-  Install futures backport on python2
-  Fix py3 unit test failure
-  Remove pypy for now from travis
-  Implement async IO writing
-  Incorporate review feedback for s3 transfers
-  Incorporate test feedback
-  Fix linting issues
-  Update review feedback from danielgtaylor
-  Remove therad safe writer, not needed anymore
-  Add support for extra_args in download_file
-  Cleanup test pep8 issues
-  Add integ test for public-read acl
-  Add code to verify allowed upload args
-  Retry stream downloads wtih get_object
-  Add migration guide for S3 and EC2
-  Review feedback
-  Remove accidental line [ci skip]
-  Update changelog [ci skip]
-  Update version, dependencies & changelog
-  Fix pep8 line spacing
-  Use string templates for readability
-  Update to final OrderedDict interface
-  Forward subset of args to upload_part calls
-  Abort multipart uploads when upload part calls fail
-  Handle fast failure shutdown cases in downloader
-  Cleanup properly on failed downloads
-  Clean up lint issues
-  Add docs to coverage, review updates.
-  Update resource models
-  Revert S3 resource update to fix bug
-  Minor doc fixes [ci skip]
-  Update developer preview notice [ci skip]
-  Handle the case where OSError is not because file does not exist
-  Merge branch 's3-high-level' into develop
-  Add S3 issues to changelog
-  Inject upload/download file to s3 clients
- ... e mais 7 commits
