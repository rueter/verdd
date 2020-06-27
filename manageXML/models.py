import string

from django.contrib.auth.models import User
from django.db.models import Q
from django.urls import reverse
from django.utils.text import slugify
from simple_history.models import HistoricalRecords

from wiki.semantic_api import SemanticAPI
from .common import Rhyme
from .constants import *
from .fields import *
from .managers import *


class DataFile(models.Model):
    lang_source = models.CharField(max_length=3)
    lang_target = models.CharField(max_length=3)
    name = models.CharField(max_length=250)
    added_date = models.DateTimeField('date published', auto_now_add=True)

    def __str__(self):
        return "%s (%d)" % (self.name, self.id)


class Language(models.Model):
    id = models.CharField(max_length=3, unique=True, primary_key=True)  # ISO 639-3
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.id

    def __repr__(self):
        return self.id


class Symbol(models.Model):
    name = BinaryCharField(max_length=250, unique=True)
    comment = models.CharField(max_length=250, blank=True)


class Lexeme(models.Model):
    class Meta:
        unique_together = ('lexeme', 'pos', 'homoId', 'language',)

    lexeme = BinaryCharField(max_length=250)
    homoId = models.IntegerField(default=0)
    assonance = models.CharField(max_length=250, blank=True)
    assonance_rev = models.CharField(max_length=250, blank=True)
    consonance = models.CharField(max_length=250, blank=True)
    consonance_rev = models.CharField(max_length=250, blank=True)
    lexeme_lang = BinaryCharField(max_length=250, blank=True)
    language = models.ForeignKey(Language, null=True, on_delete=models.SET_NULL, related_name='lexemes')
    pos = models.CharField(max_length=25)
    imported_from = models.ForeignKey(DataFile, null=True, blank=True, on_delete=models.CASCADE)
    notes = models.CharField(max_length=250, blank=True)
    added_date = models.DateTimeField('date published', auto_now_add=True)
    contlex = models.CharField(max_length=250, blank=True)
    type = models.CharField(max_length=25, blank=True)
    lemmaId = models.CharField(max_length=250, blank=True, default='')
    inflexId = models.CharField(max_length=25, blank=True)
    inflexType = models.IntegerField(choices=INFLEX_TYPE_OPTIONS,
                                     blank=True, null=True, default=None)
    checked = models.BooleanField(default=False)
    specification = models.CharField(max_length=250, blank=True)

    deleted = models.BooleanField(default=False)
    changed_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='lexemes')
    history = HistoricalRecords()

    def __str__(self):
        return self.lexeme

    def full_str(self):
        return "{} ({})".format(self.lexeme, self.pos)

    def slug(self):
        _slug = slugify(self.lexeme) if self.lexeme.strip() else 'NA'
        return _slug if _slug else self.lexeme.strip()

    def get_absolute_url(self):
        return reverse('lexeme-detail', kwargs={'pk': self.pk})

    def get_assonance(self):
        return Rhyme.assonance(self.lexeme)

    def get_assonance_rev(self):
        return Rhyme.assonance_rev(self.lexeme)

    def get_consonance(self):
        return Rhyme.consonance(self.lexeme)

    def get_consonance_rev(self):
        return Rhyme.consonance_rev(self.lexeme)

    def get_relations(self):
        return Relation.objects.filter(Q(lexeme_from=self) | Q(lexeme_to=self))

    def inflexType_str(self):
        return INFLEX_TYPE_OPTIONS_DICT[self.inflexType] if self.inflexType in INFLEX_TYPE_OPTIONS_DICT else ''

    def get_lexeme_lang(self):
        main_str = ' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~¨ÂÄÅÕÖáâäåõöČčĐđŊŋśŠšŽžƷǤǥǦǧǨǩǮǯʒʹʼˈАаẸẹ’₋'
        _sms_str = ' !"#$%&\'()*+,-./0123456789:;<=>?@AАÂBCČƷǮDĐEẸFGǦǤHIJKǨLMNŊOÕPQRSŠTUVWXYZŽÅÄÖ[\\]^_`аaâbcčʒǯdđeẹfgǧǥhijkǩlmnŋoõpqrsštuvwxyzžåäöáś¨{|}ʹʼˈ~₋’'
        _fin_str = ' !"#$%&\'()*+,-./0123456789:;<=>?@AАBCDEFGHIJKLMNOPQRSŠTUVWXYZÅÄÖ[\\]^_₋`аabcdefghijklmnopqrsštuvwxyzåäö¨{|}ʹʼ’ˈÂČƷǮĐẸǦǤǨŊÕŽâáčʒǯđẹǧǥǩŋõśž~'

        IGNORE_CHARACTERS = ' -ʹʼˈ' + string.punctuation
        LANGUAGE_SORT = {
            'sms': dict([(x, main_str[_sms_str.index(x)]) for x in _sms_str]),
            'fin': dict([(x, main_str[_fin_str.index(x)]) for x in _fin_str]),
        }
        if self.language in LANGUAGE_SORT:
            sort_dict = LANGUAGE_SORT[self.language]
            # return ''.join([sort_dict[c] if c in sort_dict else c for c in self.lexeme.upper()])
            return ''.join([sort_dict[c] for c in self.lexeme.upper() if c in sort_dict and c not in IGNORE_CHARACTERS])
        return self.lexeme

    def find_akusanat_affiliation(self):
        semAPI = SemanticAPI()
        r1 = semAPI.ask(query=(
            '[[%s:%s]]' % (self.language.capitalize(), self.lexeme), '?Category', '?POS', '?Lang',
            '?Contlex')
        )

        if 'query' in r1 and 'results' in r1['query'] and r1['query']['results']:
            title, info = r1['query']['results'].popitem()
            return title
        return None

    def save(self, *args, **kwargs):
        # store rhyming features
        self.assonance = self.get_assonance()
        self.assonance_rev = self.get_assonance_rev()
        self.consonance = self.get_consonance()
        self.consonance_rev = self.get_consonance_rev()
        self.lexeme_lang = self.get_lexeme_lang()

        # automatically get the inflexType
        if (not self.inflexType or self.inflexType == 0) and self.contlex:
            for inflexType, inflexType_list in INFLEX_TYPE_MAPPINGS.items():
                if self.contlex in inflexType_list:
                    self.inflexType = inflexType
                    break
            else:
                self.inflexType = INFLEX_TYPE_X

        return super(Lexeme, self).save(*args, **kwargs)

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    def metadata_str(self, sep='__'):
        _metadata = self.lexememetadata_set.order_by('text').values_list('text', flat=True)
        return sep.join(_metadata) if _metadata else ''


class Relation(models.Model):
    class Meta:
        unique_together = ('lexeme_from', 'lexeme_to', 'type')

    lexeme_from = models.ForeignKey(Lexeme, related_name='lexeme_from_lexeme_set', on_delete=models.CASCADE)
    lexeme_to = models.ForeignKey(Lexeme, null=True, blank=True, related_name='lexeme_to_lexeme_set',
                                  on_delete=models.CASCADE)
    type = models.IntegerField(choices=RELATION_TYPE_OPTIONS,
                               default=0)
    notes = models.CharField(max_length=250, blank=True)

    checked = models.BooleanField(default=False)
    added_date = models.DateTimeField('date published', auto_now_add=True)
    deleted = models.BooleanField(default=False)
    changed_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='relations')
    history = HistoricalRecords()

    def __str__(self):
        return "%s - %s" % (self.lexeme_from.lexeme,
                            self.lexeme_to.lexeme if self.lexeme_to else '')

    def full_str(self):
        return "{}  - {}".format(self.lexeme_from.full_str(), self.lexeme_to.full_str())

    def type_str(self):
        return RELATION_TYPE_OPTIONS_DICT[self.type] if self.type in RELATION_TYPE_OPTIONS_DICT else ''

    def get_absolute_url(self):
        return reverse('relation-detail',
                       kwargs={'pk': self.pk})

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value


class Source(models.Model):
    class Meta:
        unique_together = ('relation', 'name')

    relation = models.ForeignKey(Relation, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    page = models.CharField(max_length=25, blank=True)
    type = models.CharField(max_length=25)
    notes = models.CharField(max_length=250, blank=True)
    added_date = models.DateTimeField('date published', auto_now_add=True)
    changed_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='sources')
    history = HistoricalRecords()

    def __str__(self):
        return "(%s) %s" % (self.type, self.name)

    def get_absolute_url(self):
        return reverse('relation-detail',
                       kwargs={'pk': self.relation.pk})

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value


class MiniParadigm(models.Model):
    lexeme = models.ForeignKey(Lexeme, on_delete=models.CASCADE)
    msd = models.CharField(max_length=25)
    wordform = models.CharField(max_length=250)
    changed_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='miniparadigms')
    history = HistoricalRecords()

    def __str__(self):
        return "%s: %s" % (self.msd, self.wordform)

    def full_str(self):
        return "%s - %s: %s" % (self.lexeme.full_str(), self.msd, self.wordform)

    def get_absolute_url(self):
        return reverse('lexeme-detail',
                       kwargs={'pk': self.lexeme.pk})

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value


class Affiliation(models.Model):
    class Meta:
        unique_together = ('lexeme', 'title', 'link', 'type')

    lexeme = models.ForeignKey(Lexeme, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    link = models.URLField(null=True, default=None)
    type = models.IntegerField(choices=AFFILIATION_TYPES,
                               blank=True, null=True, default=None)
    checked = models.BooleanField(default=False)
    notes = models.CharField(max_length=250, blank=True)
    changed_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='affiliations')
    history = HistoricalRecords()

    def get_absolute_url(self):
        return reverse('lexeme-detail', kwargs={'pk': self.lexeme.pk})

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value


class Example(models.Model):
    class Meta:
        unique_together = ('lexeme', 'text')

    lexeme = models.ForeignKey(Lexeme, on_delete=models.CASCADE)
    text = models.CharField(max_length=250)
    changed_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='examples')
    history = HistoricalRecords()

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse('lexeme-detail', kwargs={'pk': self.lexeme.pk})

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value


class RelationMetadata(models.Model):
    class Meta:
        unique_together = ('relation', 'language', 'type', 'text')

    relation = models.ForeignKey(Relation, on_delete=models.CASCADE)
    text = models.CharField(max_length=250)
    language = models.ForeignKey(Language, null=True, on_delete=models.SET_NULL, related_name='relation_metadata')
    type = models.IntegerField(choices=RELATION_METADATA_TYPES,
                               blank=True, null=True, default=None)
    changed_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL,
                                   related_name='relation_metadata')
    history = HistoricalRecords()

    def __str__(self):
        return "({}) {}".format(self.language, self.text)

    def get_absolute_url(self):
        return reverse('relation-detail',
                       kwargs={'pk': self.relation.pk})

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value


class RelationExample(models.Model):
    class Meta:
        unique_together = ('relation', 'language', 'text')

    relation = models.ForeignKey(Relation, on_delete=models.CASCADE)
    text = models.CharField(max_length=250)
    language = models.ForeignKey(Language, null=True, on_delete=models.SET_NULL, related_name='relation_examples')
    changed_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL,
                                   related_name='relation_examples')
    history = HistoricalRecords()

    def __str__(self):
        return "({}) {}".format(self.language, self.text)

    def get_absolute_url(self):
        return reverse('relation-detail',
                       kwargs={'pk': self.relation.pk})

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value


class LexemeMetadata(models.Model):
    class Meta:
        unique_together = ('lexeme', 'text',)

    lexeme = models.ForeignKey(Lexeme, on_delete=models.CASCADE)
    text = models.CharField(max_length=250)
    changed_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL,
                                   related_name='lexeme_metadata')
    history = HistoricalRecords()

    def __str__(self):
        return "{}".format(self.text)

    def get_absolute_url(self):
        return reverse('lexeme-detail',
                       kwargs={'pk': self.lexeme.pk})

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value


class Stem(models.Model):
    class Meta:
        unique_together = ('lexeme', 'text', 'contlex')

    lexeme = models.ForeignKey(Lexeme, on_delete=models.CASCADE)
    text = BinaryCharField(max_length=250)
    homoId = models.IntegerField(default=0)
    contlex = models.CharField(max_length=250, blank=True)
    notes = models.CharField(max_length=250, blank=True)
    order = models.IntegerField(default=0)
    status = models.CharField(max_length=250, blank=True)

    checked = models.BooleanField(default=False)
    added_date = models.DateTimeField('date published', auto_now_add=True)
    changed_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='stems')
    history = HistoricalRecords()

    def get_absolute_url(self):
        return reverse('stem-detail', kwargs={'pk': self.pk})

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

# class StemAffiliation(models.Model):
#     class Meta:
#         unique_together = ('stem',)
#
#     stem = models.ForeignKey(Stem, on_delete=models.CASCADE)
#     title = models.CharField(max_length=250)
#     link = models.URLField(null=True, default=None)
#     type = models.IntegerField(choices=AFFILIATION_TYPES,
#                                blank=True, null=True, default=None)
#     checked = models.BooleanField(default=False)
#     notes = models.CharField(max_length=250, blank=True)
#     changed_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='affiliations')
#     history = HistoricalRecords()
#
#     def get_absolute_url(self):
#         return reverse('lexeme-detail', kwargs={'pk': self.lexeme.pk})
#
#     @property
#     def _history_user(self):
#         return self.changed_by
#
#     @_history_user.setter
#     def _history_user(self, value):
#         self.changed_by = value
