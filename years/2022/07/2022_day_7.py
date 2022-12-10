import dataclasses
from typing import Optional

# coupla constants
BASH = "$"
CD = "cd"
LS = "ls"
PREVIOUS = ".."
ROOT = "/"
DIR = "dir"
DISK_SIZE = 70_000_000
UPDATE_SIZE = 30_000_000


def partition_ls_output_into_files_and_directories(
    cwd: "Directory", ls_output: list[str]
) -> tuple[dict[str, int], dict[str, "Directory"]]:
    files: dict[str, int] = {}
    directories: dict[str, "Directory"] = {}
    for line in ls_output:
        stripped_line = line.strip()
        if stripped_line.startswith(DIR):
            # assume this is a directory - the expected format is `dir <dirname>`
            dirname = stripped_line.split(" ", 1)[1]
            directories[dirname] = Directory(name=dirname, files={}, children={}, parent=cwd)
        else:
            # assume this is a file - the expected format is `<size> <filename>`
            filesize_string, filename = stripped_line.split(" ")
            files[filename] = int(filesize_string)
    return files, directories


@dataclasses.dataclass
class Directory:
    name: str
    files: dict[str, int]
    children: dict[str, "Directory"]
    parent: Optional["Directory"] = None

    def get_absolute_parent(self) -> "Directory":
        if self.parent is None:
            return self
        return self.parent.get_absolute_parent()

    def get_all_child_directories(self) -> list["Directory"]:
        children = list(self.children.values())
        all_children = [*children]
        for child in children:
            all_children += child.get_all_child_directories()
        return all_children

    def get_total_size(self, min_file_size: int | None = None, max_file_size: int | None = None) -> int:
        # includes the size of child directories
        total_size_of_files_in_directory = sum(
            list(
                filter(
                    lambda x: (
                        (min_file_size is None or x >= min_file_size) and (max_file_size is None or x <= max_file_size)
                    ),
                    self.files.values(),
                )
            )
        )
        return total_size_of_files_in_directory + sum([child.get_total_size() for child in self.children.values()])

    @classmethod
    def from_input_file(cls, file_name: str = "input.txt") -> "Directory":
        with open(file_name, "r") as f:
            file_contents = f.read()
            file_contents_by_instruction = file_contents.split(BASH)

            root_directory = Directory(name=ROOT, files={}, parent=None, children={})
            cwd = root_directory  # hopefully this doesn't become problematic in part two!

            for instruction_line in file_contents_by_instruction:
                if stripped_instruction_line := instruction_line.strip():  # ignore empty lines
                    instruction_lines = stripped_instruction_line.splitlines()
                    # assume the first element of `instruction_lines` is the instruction and any subsequent lines are
                    # the console output
                    assert len(instruction_lines) > 0, "would be silly if this assumption is violated"
                    instruction = instruction_lines[0]

                    if instruction.startswith(CD):
                        # we changing directory
                        directory_name = instruction.split(" ", 1)[1]
                        if directory_name == ROOT:
                            cwd = root_directory
                        elif directory_name == PREVIOUS:
                            # change into the parent of this directory
                            if cwd.parent is not None:  # trying to `cd ..` from root does nothing
                                cwd = cwd.parent
                        else:
                            # change into a directory relative to this directory
                            # hopefully we don't need to handle changing into /a/b!
                            if directory_name in cwd.children.keys():
                                # change into a known directory
                                cwd = cwd.children[directory_name]
                            else:
                                # we have discovered a new directory!
                                cwd.children[directory_name] = Directory(
                                    name=directory_name, files={}, children={}, parent=cwd
                                )
                    elif instruction.startswith(LS):
                        # we printing the contents of a directory
                        files, directories = partition_ls_output_into_files_and_directories(
                            cwd=cwd, ls_output=instruction_lines[1:]
                        )
                        cwd.files |= files
                        cwd.children |= directories
                    else:
                        raise Exception(f"unknown instruction: {instruction}")
        return root_directory

    def get_total_size_of_file_system_in_range(
        self, min_directory_size: int = 0, max_directory_size: int = 100_000
    ) -> int:
        root_directory = self.get_absolute_parent()
        total_size = sum(
            filter(
                lambda x: min_directory_size <= x <= max_directory_size,
                [x.get_total_size() for x in root_directory.get_all_child_directories()],
            )
        )
        return total_size

    def find_one_directory_to_delete_in_file_system(self) -> "Directory":
        root_directory = self.get_absolute_parent()
        root_directory_size = root_directory.get_total_size()
        current_unused_space = DISK_SIZE - root_directory_size
        required_space = UPDATE_SIZE - current_unused_space
        assert required_space > 0, "You already have enough space for the update!"
        smallest_big_directory = min(
            filter(
                lambda x: x[1] >= required_space,
                [(x, x.get_total_size()) for x in root_directory.get_all_child_directories()],
            ),
            key=lambda x: x[1],
        )[0]
        return smallest_big_directory


if __name__ == "__main__":
    file_system = Directory.from_input_file()
    print(
        "The total file size of files with size of at most 100,000 is "
        f"{file_system.get_total_size_of_file_system_in_range(max_directory_size=100_000)}."
    )
    one_directory_to_delete = file_system.find_one_directory_to_delete_in_file_system()
    print(
        f"You should delete directory '{one_directory_to_delete.name}' "
        f"(which has size {one_directory_to_delete.get_total_size()})."
    )
