from django.db import migrations

TRIGGER = '''
CREATE OR REPLACE FUNCTION set_bool_when_offline_picture_changes()
RETURNS trigger AS $$
BEGIN
    IF (NEW.offline_picture IS DISTINCT FROM OLD.offline_picture) THEN
        NEW.is_image_edited := TRUE;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER set_image_edited
BEFORE INSERT OR UPDATE ON public.patients
FOR EACH ROW
EXECUTE FUNCTION set_bool_when_offline_picture_changes();
'''

REVERSE='''
DROP TRIGGER IF EXISTS set_image_edited ON public.patients;
DROP FUNCTION IF EXISTS set_bool_when_offline_picture_changes();
'''

class Migration(migrations.Migration):
    dependencies = [
        ("api", "0018_patient_is_image_edited")
    ]

    operations = [
        migrations.RunSQL(TRIGGER, REVERSE)
    ]



