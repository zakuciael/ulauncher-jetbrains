""" Contains parser for JetBrains IDEs "Recent projects" files """

import glob
import os
from typing import Optional, cast, List, TypedDict
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

from data.IdeKey import IdeKey
from data.IdeProject import IdeProject

EntryData = TypedDict("EntryData", {"path": str, "timestamp": Optional[int]})

TIMESTAMP_XML_PATH = 'value/RecentProjectMetaInfo/option[@name="projectOpenTimestamp"]'
RECENT_PROJECTS_MANAGER_PATH = './/component[@name="RecentProjectsManager"][1]'
RECENT_DIRECTORY_PROJECTS_MANAGER_PATH = \
    './/component[@name="RecentDirectoryProjectsManager"][1]'


# pylint: disable=too-few-public-methods
class RecentProjectsParser:
    """ Parser for JetBrains IDEs "Recent projects" files """

    @staticmethod
    def parse(file_path: str, ide_key: IdeKey) -> List[IdeProject]:
        """
        Parses the "Recent projects" file
        :param file_path: The path to the file
        :param ide_key: IDE key identified with the file
        :return: Parsed projects
        """

        if not os.path.isfile(file_path):
            return []

        root = ElementTree.parse(file_path).getroot()

        raw_projects = \
            root.findall(
                f'{RECENT_PROJECTS_MANAGER_PATH}/option[@name="recentPaths"]/list/option'
            ) + \
            root.findall(
                f'{RECENT_DIRECTORY_PROJECTS_MANAGER_PATH}/option[@name="recentPaths"]/list/option'
            ) + \
            root.findall(
                f'{RECENT_PROJECTS_MANAGER_PATH}/option[@name="additionalInfo"]/map/entry'
            ) + \
            root.findall(
                f'{RECENT_DIRECTORY_PROJECTS_MANAGER_PATH}/option[@name="additionalInfo"]/map/entry'
            ) + \
            root.findall(
                f'{RECENT_PROJECTS_MANAGER_PATH}/option[@name="groups"]/list/ProjectGroup/' +
                'option[@name="projects"]/list/option'
            )

        projects: List[EntryData] = [
            cast(
                EntryData,
                {
                    "path": (
                        project.attrib['value' if 'value' in project.attrib else 'key'])
                        .replace("$USER_HOME$", "~"),
                    "timestamp": (
                        int(cast(Element, project.find(TIMESTAMP_XML_PATH)).attrib["value"])
                        if project.find(TIMESTAMP_XML_PATH) is not None else None
                    ) if project.tag == "entry" else None
                }
            ) for project in raw_projects
        ]

        filtered: List[EntryData] = []
        for project in projects:
            index = next(
                (index for index, d in enumerate(filtered) if d["path"] == project["path"]),
                None
            )

            if index is None:
                filtered.append(project)
            elif index is not None and project["timestamp"] is not None:
                filtered[index]["timestamp"] = project["timestamp"]

        output = []
        for data in filtered:
            full_path = os.path.expanduser(data["path"])
            name_file = full_path + '/.idea/.name'
            name = ''

            if os.path.exists(name_file):
                with open(name_file, 'r', encoding="utf8") as file:
                    name = file.read().replace('\n', '')

            icons = glob.glob(os.path.join(full_path, '.idea', 'icon.*'))

            output.append(IdeProject(
                name=name or os.path.basename(data["path"]),
                ide=ide_key,
                path=data["path"],
                timestamp=data["timestamp"],
                icon=cast(Optional[str], icons[0] if len(icons) > 0 else None),
            ))

        return output
