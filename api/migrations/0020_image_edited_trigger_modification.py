from django.db import migrations
TRIGGER = '''
-- Reverse migration 19
DROP TRIGGER IF EXISTS set_image_edited ON public.patients;
DROP FUNCTION IF EXISTS set_bool_when_offline_picture_changes();

CREATE OR REPLACE FUNCTION set_true_when_picture_changes()
RETURNS trigger AS $$
BEGIN
    IF (NEW.offline_picture IS DISTINCT FROM OLD.offline_picture)
    OR (NEW.picture IS DISTINCT FROM OLD.picture) THEN
        NEW.is_image_edited := TRUE;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER set_image_edited
BEFORE INSERT OR UPDATE ON public.patients
FOR EACH ROW
EXECUTE FUNCTION set_true_when_picture_changes();
'''

REVERSE = '''
DROP TRIGGER IF EXISTS set_image_edited ON public.patients;
DROP FUNCTION IF EXISTS set_true_when_picture_changes();
'''


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0019_image_edited_trigger")
    ]

    operations = [
        migrations.RunSQL(TRIGGER, REVERSE)
    ]



