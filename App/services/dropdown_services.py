from App.repositories.dropdown_repository import DropdownRepository

class DropdownService:
    @staticmethod
    def get_dropdown_by_group(group_text: str):
        return DropdownRepository.get_dropdown_items(group_text)
