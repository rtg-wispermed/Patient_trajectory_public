### Instructions on working with git in command line

- To see if you are actually inside a working tree

```
git rev-parse --is-inside-work-tree
```

This will return true if you are. You can also check whether your folder has .git file.

- To see the top level of the local git repository

```
git rev-parse --show-toplevel

```

- Let's say you do not have local repository you would clone this repository like so

```
git clone https://github.com/bahadirery/Wispermed.git

```
This will initialize the git and download all the content from default branch.

- There may be a case that you have all the files from repo but .git file does not exist. Namely, your folder is not a local repository. You would this steps to make it local repository.
```
git init 

git remote add Wispermed https://github.com/bahadirery/Wispermed.git

```

- A popular case: You worked on your local repository and you want to push the changes. The pattern would be so: pull > add > commit > push 

First you can check the status. This will show whether origin is ahead of you or not. Or,  there may be some changes on your local repo. This command will give you an overview.

```
git status
```
Assume, someone else made some changes before you and commited them. You would want to update your local repository.( Actually it makes sense to do it before start working because we are small group and no one would write a code that conflicts with other codes.) Run command:

```
git pull Wispermed main

```
Then, you stage your changes. The '.' means you want to stage all of your changes.

```
git add .
```
You can commit your staged changes with commit message. 
```
git commit -m "your commit message"
```
Lastly, you must push your commit to the main branch.

```
git push Wispermed main
```

If there is no conflicting code, above commands should work. However, if you think the you should modify (or modified) the code in a way that it would conflict, here is how to create a new branch and start a pull request to be compared and merged with the main branch.

The pattern:
- Create new branch
- Switch to new branch
- Make changes
- Commit
- Push


```
git branch <new-branch-name>

git checkout <new-branch-name>

git commit -am "message"

git push origin <new-branch-name>
```
You can then see the pull request on GitHub website  and compare the codes. 

#### How to write a code that does not conflicts with others code so that we would not worry about merging:
- Basically, we should not delete the any code. We should build top of the existing code. Commenting is a good way to go. 
