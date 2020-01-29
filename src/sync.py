import differ
import os
import source
import youtube
    

def main(source_dir, dry_run = True):
    print('Loading expected playlist config from source...')
    expected = source.Client(source_dir).get_playlists()

    print('Fetching actual playlist config from YouTube...')
    yt = youtube.Client.from_environment()
    actual = yt.get_playlists()

    print('Calculating difference...')
    ops = list(differ.diff(expected, actual))

    if len(ops) == 0:
        print('Nothing to do!')
        return

    print('')
    print('This is what we\'re going to do:')
    print('')
    for op in ops:
        print(op)
        print('')

    if dry_run:
        print('Halting; dry-run mode enabled.')
        return

    print('Applying...')
    for op in ops:
        yt.apply(op)
    print('Done!')

if __name__ == '__main__':
    main(
        source_dir = '.',

        # Only apply the operations on master commits
        # TODO: should probably make this use argparse instead of magic envvars
        dry_run = os.environ.get('GITHUB_REF') != 'refs/heads/master',
    )
