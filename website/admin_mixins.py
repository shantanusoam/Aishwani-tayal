from tinymce.widgets import AdminTinyMCE


class RichTextAdminMixin:
    """Attach TinyMCE to declared TextField names in Django admin."""

    rich_text_fields: tuple[str, ...] = ()

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name in self.rich_text_fields:
            kwargs["widget"] = AdminTinyMCE()
        return super().formfield_for_dbfield(db_field, request, **kwargs)
