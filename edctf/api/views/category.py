from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from edctf.api.models import Ctf, Challengeboard, Category
from edctf.api.serializers import CategorySerializer
from edctf.api.serializers.admin import CategorySerializer as AdminCategorySerializer
from edctf.api.permissions import CategoryPermission, CategoryPermissionDetail
from response import error_response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response


class CategoryView(APIView):
  """
  Manages category requests.
  """
  permission_classes = (CategoryPermission,)

  def get(self, request, format=None):
    """
    Gets all categories
    """
    categories = Category.objects.all()

    if request.user.is_staff:
      serialized_categories = AdminCategorySerializer(categories, many=True, context={'request': request})
    else:
      serialized_categories = CategorySerializer(categories, many=True, context={'request': request})
    return Response({
      'categories': serialized_categories.data,
    })

  def post(self, request, format=None):
    """
    Create a new category
    """
    if 'category' not in request.data or not request.data['category']:
      return error_response('Category not given')

    category_data = request.data['category']
    if 'challengeboard' not in category_data or not category_data['challengeboard']:
      return error_response('Category challengeboard not given', errorfields={'challengeboard': True})
    if 'name' not in category_data or not category_data['name']:
      return error_response('Category name not given', errorfields={'name': True})

    if len(category_data['name']) > 50:
      return error_response('Category name too long, over 50 characters', errorfields={'name': True})

    try:
      challengeboard_id = int(category_data['challengeboard'])
    except ValueError:
      return error_response('Challengeboard not found', errorfields={'challengeboard': True})

    try:
      challengeboard = Challengeboard.objects.get(id=challengeboard_id)
    except ObjectDoesNotExist:
      return error_response('Challengeboard not found', errorfields={'challengeboard': True})

    name = str(category_data['name'])
    if challengeboard.categories.filter(name__iexact=name).exists():
      return error_response('Category name already taken', errorfields={'name': True})

    try:
      category = Category.objects.create(name=name, challengeboard=challengeboard)
    except IntegrityError:
      return error_response('Category name already taken', errorfields={'name': True})

    serialized_category = CategorySerializer(category, many=False, context={'request': request})
    return Response({
      'category': serialized_category.data,
    })


class CategoryViewDetail(APIView):
  """
  Manages category by id requests.
  """
  permission_classes = (CategoryPermissionDetail,)

  def get(self, request, id, format=None):
    """
    Gets individual category via id
    """
    try:
      category = Category.objects.get(id=id)
    except ObjectDoesNotExist:
      return error_response('Category not found')

    if request.user.is_staff:
      serialized_category = AdminCategorySerializer(category, many=False, context={'request': request})
    else:
      serialized_category = CategorySerializer(category, many=False, context={'request': request})
    return Response({
      'category': serialized_category.data,
    })

  def put(self, request, id, format=None):
    """
    Edits a category
    """
    try:
      category = Category.objects.get(id=id)
    except ObjectDoesNotExist:
      return error_response('Category not found')

    if 'category' not in request.data or not request.data['category']:
      return error_response('Category not given')

    category_data = request.data['category']
    if 'name' not in category_data or not category_data['name']:
      return error_response('Category name not given', errorfields={'name': True})

    if len(category_data['name']) > 50:
      return error_response('Category name too long, over 50 characters', errorfields={'name': True})

    name = str(category_data['name'])
    if category.challengeboard.categories.exclude(id=category.id).filter(name__iexact=name).exists():
      return error_response('Category name already taken', errorfields={'name': True})

    category.name = name;
    try:
      category.save()
    except IntegrityError:
      return error_response('Category name already taken', errorfields={'name': True})

    serialized_category = CategorySerializer(category, many=False, context={'request': request})
    return Response({
      'category': serialized_category.data,
    })

  def delete(self, request, id, format=None):
    """
    Deletes a category
    """
    try:
      category = Category.objects.get(id=id)
    except ObjectDoesNotExist:
      return error_response('Category not found')
    category.delete()
    return Response({})
